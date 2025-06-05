from typing import Optional, List
from .base import ZenicogBaseModel


class UserItem(ZenicogBaseModel):
    id: str
    name: str
    userEmail: str


class ListUsersItems(ZenicogBaseModel):
    totalCount: Optional[int]
    items: Optional[List[UserItem]]


class UserDetail(UserItem):
    birthFormat: str
    isChangedPWD: bool
    isConsentSignedMsg: bool = None


class ListUsersDetails(ZenicogBaseModel):
    pageLength: Optional[int]
    items: Optional[List[UserDetail]]
