from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from todo_app.models import TaskWithId, UpdateTask, Task
from todo_app.operations import read_all_tasks, read_task_by_id, create_task, modify_task, remove_task
from todo_app.security import fake_users_db, UserInDB, fakely_hash_password, fake_token_generator, User, \
    get_user_from_token

tasks_router = APIRouter(prefix='/tasks')

@tasks_router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fakely_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = fake_token_generator(user)

    return {"access_token": token, "token_type": "bearer"}

@tasks_router.get('/', response_model=list[TaskWithId])
def get_tasks(status: Optional[str] = None, title: Optional[str] = None):
    tasks = read_all_tasks()
    if status:
        tasks = [task for task in tasks if task.status == status]
    if title:
        tasks = [task for task in tasks if task.title == title]
    return tasks

@tasks_router.get('/{id}', response_model=TaskWithId)
def get_task_by_id(id: int):
    task = read_task_by_id(id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@tasks_router.post('/', response_model=TaskWithId)
def create_task_api(task: Task):
    return create_task(task)

@tasks_router.get('/search', response_model=list[TaskWithId])
def search_tasks(query: str):
    tasks = read_all_tasks()
    filtered_tasks = [
        task for task in tasks if query.lower() in (task.title + task.description).lower()
    ]
    return filtered_tasks


@tasks_router.put('/{id}', response_model=TaskWithId)
def update_task(id: int, task_update: UpdateTask):
    modified = modify_task(id, task_update.model_dump(exclude_unset=True))
    if not modified:
        raise HTTPException(status_code=404, detail="Task not found")
    return modified

@tasks_router.delete('/{id}', response_model=Task)
def delete_task(id: int):
    deleted = remove_task(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted

@tasks_router.get("/users/me", response_model=User)
def reade_me(current_user: User = Depends(get_user_from_token)):
    return current_user
