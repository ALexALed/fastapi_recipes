from fastapi import APIRouter

from validation_and_serialization.models import InputModel

validation_and_serialization_router = APIRouter(prefix='/validation_and_serialization')

@validation_and_serialization_router.post('/test')
def validation_and_serialization_test(input: InputModel):
    return {'sent': input}