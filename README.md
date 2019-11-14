# UserManagement

##### Run
This a test project with **Flask**. Using **Postgres** as Database.

by running command below it will comes up on **Docker** and will be accessible through `localhost:8000`.

`docker-compose up --build`

It'll create an admin user on start up with following credentials if it's not exists:
  - **Username:** `admin`
  - **Password:** `123qwe!@#`

---
##### Postman
You can use added Postman collection to see and work with the web services.
Please create an Environment and add `server_url` as variable in the environment.

---
##### Packages
I used
  - **Flask-SQLAlchemy** as ORM
  - **Marshmallow** as ODM
  - **Gunicorn** as Server

---
##### Test
You can connect to bash of the project and run test with following commands:
  - `docker-compose exec project bash`
  - `pytest`

for seeing coverage in html run:
  - `coverage run -m pytest`
  - `coverage html`
  
this will create a directory named `htmlcov` and by opening `index.html` in your browser you will see report.

---
##### Git Development Flow
For every web service I created a branch and after testing was done I merge that branch into `master` and then deleted that branch.
Branches were:
- `register-webservice`
- `login-webservice`
- `user-create-webservice`
- `user-list-webservice`
- `user-update-webservice`
- `user-get-webservice`
- `user-delete-webservice`
