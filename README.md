**저장소 구조 열거**

저장소 파일 목록을 먼저 생각해 보았습니다. API를 통해 직접 가져오기보다는 수동으로 폴더 구조를 그려보는 것이 더 쉽다고 느꼈습니다. 루트 폴더에는 `.gitignore`, `README.md`, `main.py`, `requirements.txt` 같은 파일이 있을 것입니다. `zenicog_client` 폴더 안에는 `core`, `mixins`, `schemas` 같은 하위 폴더가 있고, 각 폴더 안에는 구체적인 파일들이 들어 있을 것으로 예상합니다. 먼저 `.gitignore`, `main.py`, `requirements.txt`를 살펴보며 자세한 내용을 확인해 보겠습니다.

---

**저장소 구조 탐색**

저장소의 파일 구조를 확인할 계획입니다. API를 사용해 가져올 수도 있겠지만, 수동으로 개략을 잡는 편이 더 간단해 보입니다. 루트에는 `.gitignore`, `README.md`, `main.py`, `requirements.txt` 같은 파일이 있을 것이고, `zenicog_client` 폴더 안에는 `core`, `mixins`, `schemas` 폴더와 그 안의 파일들이 있을 것입니다.

---

**저장소 설명 초안**

처음에는 API를 통해 저장소 목록을 가져오려 했지만, 세션 제한으로 GitHub가 차단될 수도 있어 폴더 구조를 가정하여 작성하기로 했습니다. 루트에는 `.gitignore`, `README.md`, `main.py`, `requirements.txt`가 있을 것이고, `zenicog_client` 폴더에는 `core`, `mixins`, `schemas` 같은 하위 폴더가 있습니다.

---

# MH-Backoffice

Zenicog REST API용 작은 파이썬 클라이언트 라이브러리이자 “백오피스” 예제 스크립트입니다. 주요 사용 기술:

- **`httpx`**: 비동기 HTTP 요청  
- **`pydantic`**: 응답 검증 및 파싱  
- **`python-dotenv`**: 환경 변수 기반 설정  

이 프로젝트는 다음을 보여줍니다:

- **믹스인(mixins)** 으로 관심사 분리  
- 인증, 토큰 만료 재시도, Pydantic 파싱을 처리하는 **베이스 클라이언트**  
- 모든 것을 조합하는 **예제 스크립트** (`main.py`)

---

## 🚀 빠른 시작

1. **클론 및 설치**  
   ```bash
   git clone https://github.com/danielkim719/mh-backoffice.git
   cd mh-backoffice
   python -m venv .venv
   source .venv/bin/activate    # Linux/macOS
   .venv\Scripts\activate       # Windows PowerShell

   pip install -r requirements.txt


2. **프로젝트 루트에 `.env` 파일 생성**

   ```dotenv
   ZENICOG_TOKEN=eyJhbG…           # 초기 Firebase 액세스 토큰
   ZENICOG_PROFILE=e5c04699-…      # 프로파일 ID
   ZENICOG_BASE_URL=https://…     # API 기본 URL (스테이지 또는 프로덕션)
   ZENICOG_USER_ID=you@domain.com  # (선택) 410 에러 시 자동 리프레시용
   ZENICOG_USER_PW=yourpassword    # (선택) 410 에러 시 자동 리프레시용
   ```

3. **예제 실행**

   ```bash
   python main.py
   ```

   이 스크립트는 아래를 수행합니다:

   1. 인증 (토큰/프로필 사용)
   2. **내 사용자 정보** 조회
   3. `ZENICOG_ORG_ID` 환경변수에 지정된 **특정 조직의 사용자 목록** 조회
   4. **전체 조직 목록** 조회
   5. 콘솔에 JSON 출력

---

## 📂 폴더 구조

```
mh-backoffice/
├── .gitignore
├── main.py                  # 예제 / 통합 테스트 스크립트
├── README.md
├── requirements.txt
└── zenicog_client/          # 재사용 가능한 클라이언트 패키지
    ├── __init__.py
    ├── client.py            # 최종 `ZenicogClient` 클래스
    ├── core/
    │   └── base_client.py   # HTTP + 인증 + 재시도 + Pydantic 파싱
    ├── mixins/
    │   ├── auth_mixin.py        # login(), my(), get_user()
    │   ├── user_mixin.py        # list_users(), get_user_detail()
    │   └── organization_mixin.py# list_organizations(), get_organization()
    └── schemas/
        ├── base.py              # 공통 Pydantic 설정
        ├── auth.py              # LoginResponse, AccessUser, AccessUserProfile
        ├── user.py              # UserItem, UserDetail, ListUsers…
        └── organization.py      # OrganizationItem, OrganizationDetail, ListOrganizations…
```

---

## 🔍 코드 설명

### 1. `core/base_client.py`

**`ZenicogBaseClient`**

* `token`과 `profile` 헤더를 가진 `httpx.AsyncClient` 생성
* 단일 `async request(...)` 메서드 제공:

  1. HTTP 요청 전송
  2. **`410`** (토큰 만료) & `_retry=True`인 경우, `self.login()` 호출해 토큰 갱신
  3. 요청을 한 번 더 재전송
  4. JSON 파싱, `model`이 지정된 경우 `model.parse_obj(raw)`

**설계 이유**

* 재시도 및 인증 로직을 한 곳에 모아두기
* 믹스인이나 서브클래스가 `login()`만 구현하면 흐름을 건드리지 않고 확장 가능

### 2. `mixins/auth_mixin.py`

* **`login(user_id, user_pw)`**: `POST /auth/web-login-v2` 호출 후 `self.token`, `self.profile` 갱신
* **`my()`**: `GET /staff/my` → `AccessUser` 반환
* **`get_user(user_id)`**: `GET /staff/user/{user_id}` → `AccessUserProfile` 반환

**핵심 결정**

* 자격증명은 `.env`에만 저장하고, `login()`이 만료 시 자동 갱신 가능

### 3. `mixins/user_mixin.py` & `mixins/organization_mixin.py`

**`UserMixin`**

* `list_users(org_id, params)` → `ListUsersItems` (`items: List[UserItem]`)
* `get_user_detail(user_id)` → `UserDetail`

**`OrganizationMixin`**

* `list_organizations(params)` → `ListOrganizationsItems`
* `get_organization(org_id)` → `OrganizationDetail`

**믹스인 사용 이유**

* 각 API 영역을 작고 집중된 파일로 분리
* 새로운 API 영역 추가 시 베이스 클라이언트 변경 없이 믹스인만 추가

### 4. `client.py`

**`ZenicogClient`**

* 아래를 조합한 클래스:

  ```python
  class ZenicogClient(
      AuthMixin,
      UserMixin,
      OrganizationMixin,
      ZenicogBaseClient
  )
  ```
* `__init__`에서 `ZENICOG_*` 환경변수 읽어 초기화
* `login`, `my`, `list_users`, `list_organizations` 등 모든 메서드 상속

**커뮤니티와 전통적 관점**

* 파이썬 패키징 관례 준수
* I/O(베이스 클라이언트)와 비즈니스 로직(믹스인) 분리
* 초심자도 쉽게 따라올 수 있는 구조

### 5. `main.py`

간단한 “스모크 테스트” 예제:

```python
async def main():
    client = ZenicogClient()

    me       = await client.my()
    print("내 정보    :", me.dict())

    me_detail = await client.get_user(me.id)
    print("내 상세 정보:", me_detail.dict())

    users    = await client.list_users(os.getenv("ZENICOG_ORG_ID"), {"page":1,"itemLength":10})
    print("사용자 목록 :", [u.dict() for u in users.items])

    orgs     = await client.list_organizations({"page":1,"perPage":10})
    print("조직 목록   :", [o.dict() for o in orgs.items])
```

* 환경변수만 설정하면 **추가 보일러플레이트 없이** 바로 사용 가능
* `response.raise_for_status()`를 통한 에러 처리 예시

---

## 🔨 설계 원칙

1. **단일 HTTP 로직**

   * 하나의 `request()` 메서드가 인증, 재시도, 파싱을 모두 처리
2. **믹스인 기반 기능 모듈화**

   * API 영역별로 파일 분리 → 확장성·유지보수성 향상
3. **Pydantic으로 안정성 확보**

   * `/schemas` 에 엄격한 타입 검증
4. **환경변수 기반 설정**

   * 민감 정보 코드에 포함 금지, `.env`로 관리
5. **전면 비동기(async)**

   * `httpx.AsyncClient`로 다양한 비동기 프레임워크와 통합 용이

---

## 🤝 기여

이슈나 풀 리퀘스트 환영합니다. Zenicog 기반 백오피스나 CLI 도구 템플릿으로 자유롭게 사용하세요!

---

## 📧 연락처

Daniel Kim
질문이나 아이디어가 있으면 언제든지 연락 주세요!

```
```
