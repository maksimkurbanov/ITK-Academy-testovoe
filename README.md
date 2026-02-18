# ITK-Academy-testovoe

Simple backend project with CRU(~~D~~) (no Delete 😊) for wallet storage and manipulation.
Goal of it's creation was to develop and deepen knowledge and skills working with modern backend development tools
in async paradigm.  

#### Core technologies
- FastAPI - web framework for building APIs with Python 3.8+ based on standard Python type hints.
- SQLAlchemy - Object Relational Mapper
- Pydantic -  Data validation library for Python and FastAPI models
- Uvicorn - ASGI web server implementation for Python
- Alembic - lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python.
- Docker - tool to package and run an application in a loosely isolated environment
- Docker Compose - tool for defining and running multi-container Docker applications
- Postgres - open source object-relational database
- For testing:
    - pytest
- For development
    - ruff
    - uv
    - venv

### Implemented functionalities, bits and bobs
- Read & Update Endpoints
- Separate databases and env for testing and development
- CRU~~D~~ service for reading and updating items in database
- ORM Objects representing SQL tables and relationships
- Pydantic schemas
- Tests to cover implemented endpoints (with setup-and-teardown of data for test isolation)
- Docker Compose file with 3 container setup (app + production database + testing database)
  and initial Alembic migration run command
- Verbose doc-strings


## How to run

### You should have
- Running Docker

clone repository:

```bash
git clone https://github.com/maksimkurbanov/ITK-Academy-testovoe.git
```

run Docker command:
```bash
docker compose up --build -d app
```

to down and discard containers:
```bash
# use -v flag to destroy volumes attached to containers
docker compose down -v
# or run without -v for data in associated databases to persist
docker compose down
```

### It is possible to check auto-generated documentation as well as interact with app's API via SwaggerUI. 
To do that navigate to http://localhost:8000/docs (you app needs to run)

Package configurations are managed via pyproject.toml file
(no requirements.txt)