from fastapi import APIRouter

items_router = APIRouter(prefix='/items')

@items_router.get('/{id}')
async def get_items_by_id(id: int):
    return {'id': id}

