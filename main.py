from fastapi import FastAPI

from basics.basics import items_router
from basics.models import models_router
from databases.connect_example.main import db_router
from todo_app.main import tasks_router
from validation_and_serialization.main import validation_and_serialization_router

app = FastAPI()
app.include_router(items_router)
app.include_router(models_router)
app.include_router(db_router)
app.include_router(validation_and_serialization_router)
app.include_router(tasks_router)