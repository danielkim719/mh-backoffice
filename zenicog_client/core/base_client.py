import os
import httpx
from pydantic import BaseModel
from typing import Type, TypeVar, Any, Optional, Dict, Union

from ..schemas.auth import LoginResponse, AccessUser, AccessUserProfile

T = TypeVar("T", bound=BaseModel)


class ZenicogBaseClient:
    _ENV_USER_ID = os.getenv("ZENICOG_USER_ID")
    _ENV_USER_PW = os.getenv("ZENICOG_USER_PW")

    def __init__(
            self,
            token: str,
            profile: str,
            base_url: str,
            timeout: float = 10.0
    ):
        self.token = token
        self.profile = profile
        self.base_url = base_url
        self.timeout = timeout
        self.headers = {
            "X-Zenicog-Firebase": self.token,
            "X-Zenicog-Profile": self.profile,
            "Content-Type": "application/json"
        }
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=self.timeout
        )

    async def login(
            self,
            user_id: Optional[str] = None,
            user_pw: Optional[str] = None,
    ) -> AccessUser:
        login_id = user_id or self._ENV_USER_ID
        login_pw = user_pw or self._ENV_USER_PW
        if not login_id or not login_pw:
            raise RuntimeError("login() 호출에 필요한 ID/PW 없음")

        payload = {
            "userEmail": login_id,
            "passwd": login_pw
        }
        login_resp: LoginResponse = await self.request(
            "POST",
            "auth/web-login-v2",
            model=LoginResponse,
            json_body=payload,
            _retry=False
        )

        self.token = login_resp.accessCustomTokenDTO.accessToken
        self.profile = login_resp.profileSingleDTO.id
        self.headers["X-Zenicog-Firebase"] = self.token
        self.headers["X-Zenicog-Profile"] = self.profile
        self.client.headers = self.headers

        return AccessUser(
            id=login_resp.profileSingleDTO.id,
            name=login_resp.profileSingleDTO.userDTO.name,
            email=login_resp.profileSingleDTO.userDTO.userEmail,
            contactNumber=login_resp.profileSingleDTO.contactNumber,
            uid=login_resp.accessCustomTokenDTO.uid,
            accessToken=self.token,
            refreshToken=login_resp.accessCustomTokenDTO.refreshToken
        )

    async def request(
            self,
            method: str,
            endpoint: str,
            *,
            model: Optional[Type[T]] = None,
            params: Optional[Dict[str, Any]] = None,
            json_body: Optional[Dict[str, Any]] = None,
            _retry: bool = True
    ) -> Union[Dict[str, Any], T]:
        """
        공통 요청 메서드 (모델 파싱 옵션 포함)

        인자:
          - method: HTTP 메서드 ("GET", "POST", ...)
          - endpoint: 엔드포인트 URI (예: "staff/my", "auth/web-login-v2" 등)
          - model: Pydantic BaseModel 클래스를 넘기면 parse_obj(raw_json)을 수행하여 모델 인스턴스를 반환
                   None이면, raw JSON (dict)만 반환
          - params: URL 쿼리 파라미터
          - json_body: POST/PUT 요청 시 보낼 JSON 바디
          - _retry: 오류 재시도 횟수, 재시도 로직은 client.py에서 구현

        반환:
          - model이 None이면 raw JSON(dict)
          - model이 주어졌으면 해당 Pydantic 모델 인스턴스
        """

        response = await self.client.request(
            method,
            endpoint,
            params=params,
            json=json_body
        )

        if response.status_code == 410 and _retry:
            await self.login()
            response = await self.client.request(
                method,
                endpoint,
                params=params,
                json=json_body
            )

        response.raise_for_status()
        raw_dict = response.json()

        if model is not None:
            return model.parse_obj(raw_dict)
        return raw_dict

    async def close(self) -> None:
        """AsyncClient 세션 닫기"""
        await self.client.aclose()
