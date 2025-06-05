from typing import Optional, Any, Dict
from ..core.base_client import ZenicogBaseClient
from ..schemas.user import ListUsersItems, UserDetail


class UserMixin(ZenicogBaseClient):

    async def list_users(
            self,
            organization_id: str,
            params: Optional[Dict[str, Any]] = None
    ) -> ListUsersItems:
        return await self.request(
            "GET",
            f"staff/profile/{organization_id}",
            model=ListUsersItems,
            params=params
        )

    async def list_users_in_my_organization(
            self,
            params: Optional[Dict[str, Any]] = None
    ) -> ListUsersItems:
        return await self.request(
            "GET",
            "backoffice/profile",
            model=ListUsersItems,
            params=params
        )

    async def get_user_detail(
            self,
            user_id: str
    ) -> UserDetail:
        return await self.request(
            "GET",
            f"staff/user/{user_id}",
            model=UserDetail
        )

    async def my(self):
        return await self.request(
            "GET",
            "staff/my"
        )

    async def get_user(self, user_id: str):
        return await self.request(
            "GET",
            f"staff/user/{user_id}"
        )

# async def my(self) -> MyResponse:
#     """
#     • GET /staff/my
#     • 반환: MyResponse (Pydantic 모델)
#     """
#     raw = await self._request("GET", "staff/my")
#     return MyResponse.parse_obj(raw)
#
# async def user(self, user_id: str) -> SimpleUserResponse:
#     """
#     • GET /staff/user/{user_id}
#     • 반환: SimpleUserResponse (email 필드만)
#     """
#     raw = await self._request("GET", f"staff/user/{user_id}")
#     return SimpleUserResponse.parse_obj(raw)
