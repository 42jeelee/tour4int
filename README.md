## TOUR4INT
----
### 사용 방법
- 해당 ROOT 파일에 `.env`파일을 넣는다. ( 필수키 `SECRET_KEY`는 빠지면 안됨)

- venv 가상 환경을 만든다.
  ```
  python -m venv <가상환경명>
  ```
- 가상 환경으로 접속한다.
  + Window에서 접속하는 방법
    ```
    .\.venv\Scripts\Acticate.ps1
    ```

- 해당 명령으로 필요한 라이브러리를 설치한다.
  ```
  pip install -r requirements.txt
  ```

- 설치 완료 후 서버를 실행시켜본다.
  ```
  python manage.py runserver
  ```
