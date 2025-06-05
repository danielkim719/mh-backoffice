from typing import Optional, List
from .base import ZenicogBaseModel


class OrganizationItem(ZenicogBaseModel):
    id: str
    name: str


class ListOrganizationsItems(ZenicogBaseModel):
    totalCount: Optional[int]
    items: Optional[List[OrganizationItem]]


class OrganizationDetail(OrganizationItem):
    exclusionType: Optional[str]
    useType: Optional[str]
    emailHost: Optional[str]
    contactPersonName: Optional[str]
    contactEmail: Optional[str]
    registrationNumber: Optional[str]
    address: Optional[str]
    serviceChargePerSecond: Optional[int]


class ListOrganizationsDetails(ZenicogBaseModel):
    pageLength: Optional[int]
    items: Optional[List[OrganizationDetail]]
