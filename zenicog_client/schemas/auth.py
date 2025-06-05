from typing import List, Optional
from .base import ZenicogBaseModel

from .organization import OrganizationDetail
from .user import UserDetail


class AccessUserToken(ZenicogBaseModel):
    uid: str
    accessToken: str
    refreshToken: str


class AccessUser(AccessUserToken):
    id: str
    name: str
    email: str
    contactNumber: str


class AccessUserProfile(ZenicogBaseModel):
    id: str
    contactNumber: str
    department: Optional[str]
    employeeNumber: Optional[str]
    isPermitted: Optional[bool]
    job: Optional[str]
    memo: Optional[str]
    position: Optional[str]
    role: Optional[str]
    accessDTOs: List[Optional[dict]]
    userDTO: UserDetail
    organizationDTO: OrganizationDetail
    createdAtFormat: str


class LoginResponse(ZenicogBaseModel):
    profileSingleDTO: AccessUserProfile
    accessCustomTokenDTO: AccessUserToken
