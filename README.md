# Airport API

API service for airport managing written in DRF


## Installing using GitHub

```shell
git clone https://github.com/olena4reunited/airport-service-api.git
cd airport-service-api
python -m venv .venv
pip install -r requirements.txt

set DJANGO_SECRET_KEY=<your-secret-key>
set POSTGRES_PASSWORD=<your-postgres-password>
set POSTGRES_USER=<your-postgres-user>
set POSTGRES_DB=<your-postgres-db>
set POSTGRES_HOST=<your-postgres-host>
set POSTGRES_PORT=5432
set PGDATA=<your-postgres-path-for-loading-data>

python manage.py migrate
python manage.py loaddata airport_data.json
python manage.py runserver
```

## Setup Instructions

1. Install Docker: Ensure that Docker is installed on your machine.

2. Create your .env file: Make a copy of the content from .env.sample and save it as .env.

3. Build and Start the Application:

```shell
    docker-compose build
    docker-compose up
```

## Accessing the API

1) create user: `api/user/register/`, body:

```json
{
  "email": "your email",
  "password": "your password"
}
```

2) login via your credentials: `api/user/register/`, body:

```json
{
  "email": "your email",
  "password": "your password"
}
```

---

Include the accessToken in the Authorization header of your requests, formatted as:

```makefile
    Authorization: Bearer <your-accessToken>
```
