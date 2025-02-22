from fastapi import FastAPI

from auth.main import auth_router
from basics.basics import items_router
from basics.models import models_router
from databases.connect_example.main import db_router
from todo_app.main import tasks_router
from validation_and_serialization.main import validation_and_serialization_router
from fastapi.openapi.utils import get_openapi

app = FastAPI(title="Fast API Recipes",
              description="Fast API Recipes repo",
              version="0.1.0", )


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Customized Title",
        version="2.0.0",
        description="This is a custom OpenAPI schema",
        routes=app.routes,
    )
    # del openapi_schema["paths"]["/tasks/token"]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
app.include_router(items_router)
app.include_router(models_router)
app.include_router(db_router)
app.include_router(validation_and_serialization_router)
app.include_router(tasks_router)
app.include_router(auth_router)
