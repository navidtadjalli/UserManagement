# UserManagement

This a test project with **Flask**. Using **Postgres** as Database.

by running command below it will comes up on **Docker** and will be accessible through `localhost:8000`.

`docker-compose up --build`

---

It'll create an admin user on start up with following credentials if it's not exists:
  - **Username:** `admin`
  - **Password:** `123qwe!@#`

---

I used
  - **FlaskSQLAlchemy** as ORM
  - **Marshmallow** as ODM
  - **Gunicorn** as Server

---

You can connect to bash of the project and run test with following commands:
  - `docker-compose exec project bash`
  - `pytest`

for seeing coverage in html run:
  - `coverage run -m pytest`
  - `coverage html`
  
this will create a directory named `htmlcov` and by openning `index.html` in your browser you will see report.
