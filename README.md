# Nombre de tu Proyecto
# FastAPI Template · ![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Build](https://github.com/agarciagaray/FastAPI-CA-Template/workflows/build/badge.svg) 
[![Dependabot Status](https://img.shields.io/badge/Dependabot-active-brightgreen.svg)](https://dependabot.com)

<div>
<img src="assets/fastapi-logo.png" alt="FastAPI Logo" height="60" /> &nbsp; &nbsp;
<img src="assets/sqlalchemy-logo.png" alt="SQLAlchemy Logo" height="60" /> &nbsp; &nbsp;
<img src="assets/mysql-logo.png" alt="MySQL Logo" height="60" /> &nbsp; &nbsp;
<img src="assets/postgresql-logo.png" alt="PostgreSQL Logo" height="60" /> &nbsp; &nbsp;
<img src="assets/sqlite-logo.png" alt="SQLite Logo" height="60" /> &nbsp; &nbsp;
<img src="assets/oauth2-logo.png" alt="OAuth2 Logo" height="60" /> &nbsp; &nbsp;
<img src="assets/jwt-logo.png" alt="JWT Logo" height="60" />
</div>

# Clean Architecture Template

What's included in the template?

- Domain layer with sample entities.
- Application layer with abstractions for:
  - Example use cases
  - Cross-cutting concerns (logging, validation)
- Infrastructure layer with:
  - Authentication
  - SQLAlchemy, PostgreSQL (you can change to SQLite for development in database/core.py)
  - Rate limiting on registration
- Testing projects
  - Pytest unit tests
  - Pytest integration tests (e2e tests)

I'm open to hearing your feedback about the template and what you'd like to see in future iterations. DM me on LinkedIn or email me.

--

# Install all dependencies.
- Run `pip install -r requirements-dev.txt`

# How to run app. Using Docker with PostgreSQL.
- Install Docker Desktop
- Run `docker compose up --build`
- Run `docker compose down` to stop all services

# How to run locally without postgres or docker.
- in database/core.py change the DATABASE_URL to sqlite
- run `uvicorn src.main:app --reload`

# How to run tests.
- Run `pytest` to run all tests


Cheers!
