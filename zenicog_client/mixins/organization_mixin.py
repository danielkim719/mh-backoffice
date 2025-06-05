from typing import Optional, Any, Dict
from ..core.base_client import ZenicogBaseClient
from ..schemas.organization import ListOrganizationsItems, OrganizationDetail, ListOrganizationsDetails


class OrganizationMixin(ZenicogBaseClient):

    async def list_organizations(
            self,
            params: Optional[Dict[str, Any]] = None
    ) -> ListOrganizationsItems:
        return await self.request(
            "GET",
            "auth/organization",
            model=ListOrganizationsItems,
            params=params
        )

    async def list_organization_details(
            self,
            params: Optional[Dict[str, Any]] = None
    ) -> ListOrganizationsDetails:
        return await self.request(
            "GET",
            "auth/organization",
            model=ListOrganizationsDetails,
            params=params
        )

    async def get_organization(
            self,
            org_id: str
    ) -> OrganizationDetail:
        return await self.request(
            "GET",
            f"auth/organization/{org_id}",
            model=OrganizationDetail
        )
