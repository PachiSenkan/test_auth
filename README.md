# Simple JWT-Auth

## How to start
1. Clone repository
  ```
  git clone https://github.com/PachiSenkan/test_auth.git
  ```
3. Go to /test_auth
4. Create virtual environment
**Windows:**
  ```
  python -m venv venv
  /venv/Scripts/activate
  ```
**Linux:**
  ```
  python3 -m venv venv
  source venv/bin/sctivate
  ```
5. Install dependencies
**Windows:**
  ```
  python -m pip install -r requirements.txt
  ```
**Linux:**
  ```
  python3 -m pip install -r requirements.txt
  ```
6. Start server
  ```
  uvicorn app.main:app --reload
  ```
API is available from `127.0.0.1:8000/api/v1/` or from OpenAPI docs `127.0.0.1:8000/docs/`
