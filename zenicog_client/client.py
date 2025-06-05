import os
from dotenv import load_dotenv

load_dotenv("")

from .core.base_client import ZenicogBaseClient

from .mixins.user_mixin import UserMixin
from .mixins.organization_mixin import OrganizationMixin


class ZenicogClient(
    UserMixin,
    OrganizationMixin,
    ZenicogBaseClient
):

    def __init__(self):
        token = os.getenv("ZENICOG_TOKEN")
        profile = os.getenv("ZENICOG_PROFILE")
        base_url = os.getenv("ZENICOG_BASE_URL")

        if not base_url or not token or not profile:
            raise RuntimeError("환경변수 없음. 데이터 확인.")

        super().__init__(
            token,
            profile,
            base_url
        )
