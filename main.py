import asyncio

from zenicog_client.client import ZenicogClient


async def main():
    # 클라이언트 초기화: token/profile/base_url은 환경변수에서 자동으로 읽어옵니다.
    client = ZenicogClient()

    try:
        # # 1) 내 정보 조회 (AccessUser 형태로 반환됨)
        # me: AccessUser = await client.my()
        # print("내 정보:")
        # print(json.dumps(me.dict(), indent=2, ensure_ascii=False))
        #
        # # 2) 내 상세 정보 조회 (AccessUserProfile 형태로 반환됨)
        # #    ─ 기존 `client.user(...)` 대신 `client.get_user_detail(...)` 사용
        # me_detail: AccessUserProfile = await client.get_user(me.id)
        # print("\n내 상세 정보:")
        # print(json.dumps(me_detail.dict(), indent=2, ensure_ascii=False))

        # 3) 특정 조직(ZENICOG_ORG_ID) 사용자 목록 조회

        from dotenv import load_dotenv
        load_dotenv()
        import os
        org_id = os.getenv("ZENICOG_ORG_ID")

        if not org_id:
            raise RuntimeError("환경변수 ZENICOG_ORG_ID가 설정되어 있지 않습니다.")

        users_list = await client.list_users(organization_id=org_id, params={"page": 1, "itemLength": 10})
        # ListUsersItems 스키마를 파싱하므로, .items는 List[UserItem]
        print("\n조직 사용자 목록:")
        for u in users_list.items or []:
            print(u.dict())

        # 4) 조직 목록 조회
        orgs_list = await client.list_organizations(params={"page": 1, "perPage": 10})
        # ListOrganizationsItems 스키마를 파싱하므로, .items는 List[OrganizationItem]
        print("\n조직 목록:")
        for o in orgs_list.items or []:
            print(o.dict())

    except Exception as e:
        print("\n에러 발생:", e)
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
