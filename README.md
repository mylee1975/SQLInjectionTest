# 🛡️ SQL Injection Laboratory 2026 (Educational Lab)

이 저장소는 **SQL Injection(SQLi)** 공격의 메커니즘을 심도 있게 학습하기 위해 설계된 의도적으로 취약한(Intentionally Vulnerable) 웹 애플리케이션입니다. 학습자는 필터링되지 않은 입력값이 데이터베이스 쿼리에 미치는 영향을 직접 분석하고 익스플로잇을 수행할 수 있습니다.

---

## ⚠️ 법적 고지 (Legal Disclaimer)
> **본 프로젝트는 보안 교육 및 모의해킹 실습만을 위한 목적으로 제작되었습니다.**  
> 인가되지 않은 대상에 대한 공격은 정보통신망법 등 관련 법률에 따라 처벌받을 수 있습니다. 반드시 로컬 환경(localhost)에서만 실행하십시오. 본 소프트웨어의 오용으로 인한 책임은 사용자에게 있습니다.

---

## 📖 1. 환경 설정집 (Environment Bible)

실습 환경은 복잡한 설정 없이 즉시 실행 가능한 **Zero-Config** 철학을 따릅니다.

- **기술 스택:**
  - **Runtime:** Python 3.8+
  - **Framework:** Flask (Minimalist Web Server)
  - **Database:** SQLite3 (Serverless, File-based DB)
- **서비스 목적:** 사용자 아이디를 기반으로 회원 정보를 조회하는 '마이페이지 조회' 기능 모사.
- **취약점 지점:** `SELECT` 쿼리의 `WHERE` 절에 사용자 입력값(`username`)이 필터링 없이 직접 삽입(Concatenation).
- **데이터베이스 구성 (Database Schema):**
  - Table Name: `users`
  - Columns: `id(INT)`, `username(TEXT)`, `password(TEXT)`, `email(TEXT)`, `role(TEXT)`, `secret_note(TEXT)`
- **플래그(Flag):** `secret_note` 컬럼 내 특정 레코드에 `HACK_THE_DATABASE_2026` 포함.

---

## 🏗️ 2. 구현 가드레일 (Implementation Guardrail)

이 프로젝트는 교육적 효과를 극대화하기 위해 아래와 같은 **의도적인 보안 결함**을 유지하도록 강제됩니다.

1.  **완전 무방비 상태(Zero Protection):**
    - `ORM(SQLAlchemy 등)` 사용을 엄격히 금지합니다.
    - `Prepared Statement`나 `Parameterized Query`를 사용하지 않습니다. 오직 `f-string` 또는 문자열 더하기(+)로만 쿼리를 생성합니다.
2.  **보안 라이브러리 사용 금지:**
    - 입력값 검증을 위한 `WTForms`, `Bleach` 또는 정규표현식 필터링을 절대 적용하지 않습니다.
3.  **에러 핸들링 최소화 (Verbose Error):**
    - 데이터베이스에서 발생하는 모든 문법 에러(SQL Error)가 브라우저 화면에 그대로 노출되도록 설정합니다. (Error-based SQLi 실습 지원)
4.  **싱글 파일 지향:**
    - 로직 파악을 용이하게 하기 위해 백엔드 핵심 로직을 `app.py` 단일 파일에 집중시킵니다.
5.  **보안 헤더 비활성화:**
    - 브라우저의 기본 보안 기능(XSS Filter 등)이 실습에 방해가 되지 않도록 최소한의 헤더만 사용합니다.

---

## 🚀 3. 실습 시나리오 (Practice Steps)

### Step 1: 환경 구성
- `pip install flask` 명령어로 환경을 준비하고 `python app.py`를 실행합니다.

### Step 2: 취약점 식별
- 입력창에 싱글 쿼터(`'`)를 입력하여 `sqlite3.OperationalError`가 발생하는지 확인합니다.

### Step 3: 공격 가이드
1.  **인증 우회:** `' OR 1=1 --` 를 입력하여 모든 사용자 정보를 탈취합니다.
2.  **스키마 탐색:** `UNION SELECT`를 사용하여 데이터베이스의 테이블 구조(`sqlite_master`)를 조회합니다.
    - `Payload: ' UNION SELECT 1, tbl_name, 'info', 'schema' FROM sqlite_master WHERE type='table' --`
3.  **데이터 탈취:** 최종적으로 `secret_note` 컬럼을 조회하여 숨겨진 플래그를 획득합니다.
    - `Payload: ' UNION SELECT id, username, secret_note, role FROM users --`

---

## ✅ 4. 일관성 검증 체크리스트 (Verification Checklist)

관리자 및 개발자는 배포 전 아래 항목을 확인하여 실습 환경의 적절성을 검증하십시오.

- [x] **취약성 확보:** SQL 쿼리가 `f-string` 또는 문자열 더하기로 구현되었는가?
- [x] **에러 노출:** SQL 에러 메시지가 사용자에게 `JSON` 또는 `HTML`로 반환되는가?
- [x] **더미 데이터:** `admin` 계정과 플래그(`HACK_THE_DATABASE_2026`)가 DB에 존재하는가?
- [x] **의존성 최소화:** 외부 라이브러리 설치 없이 `pip install flask` 만으로 실행 가능한가?
- [x] **공격 작동:** 제공된 익스플로잇 페이로드가 실제 환경에서 작동하는가?

---

## 📄 라이선스
본 프로젝트는 **MIT License**에 따라 자유롭게 배포 및 수정이 가능합니다. 단, 교육 목적 이외의 사용으로 발생하는 문제에 대해서는 책임을 지지 않습니다.
