from fastapi import FastAPI

from basics.basics import items_router
from basics.models import models_router
from databases.connect_example.main import db_router

app = FastAPI()
app.include_router(items_router)
app.include_router(models_router)
app.include_router(db_router)