import csv
from typing import Optional
from todo_app.models import Task, TaskWithId

DATABASE_FILENAME = "tasks.csv"

column_fields = ['id', 'title', 'description', 'status']

def read_all_tasks() -> list[TaskWithId]:
    with open(DATABASE_FILENAME) as csvfile:
        reader = csv.DictReader(csvfile)
        return [TaskWithId(**row) for row in reader]

def read_task_by_id(id: int) -> Optional[TaskWithId]:
    tasks = read_all_tasks()
    for task in tasks:
        if task.id == id:
            return task
    return None

def get_next_id() -> int:
    try:
        with open(DATABASE_FILENAME) as csvfile:
            reader = csv.DictReader(csvfile)
            max_id = max(int(row["id"]) for row in reader)
            return max_id + 1
    except (FileNotFoundError, ValueError):
        return 1

def write_task(task: TaskWithId):
    with open(DATABASE_FILENAME, mode='a', newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_fields)
        writer.writerow(task.model_dump())


def create_task(task: Task) -> TaskWithId:
    next_id = get_next_id()
    task_with_id = TaskWithId(id=next_id, **task.model_dump())
    write_task(task_with_id)
    return task_with_id

def modify_task(id: int, task: dict) -> Optional[TaskWithId]:
    updated_task: Optional[TaskWithId] = None
    tasks = read_all_tasks()
    for number, task_ in enumerate(tasks):
        if task_.id == id:
            tasks[number] = ( updated_task ) = task_.model_copy(update=task)
    with open(DATABASE_FILENAME, mode='w', newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_fields)
        writer.writeheader()
        for task in tasks:
            writer.writerow(task.model_dump())
    if updated_task:
        return updated_task

def remove_task(id: int) -> Optional[Task]:
    deleted_task: Optional[TaskWithId] = None
    tasks = read_all_tasks()
    for number, task_ in enumerate(tasks):
        if task_.id == id:
            deleted_task = tasks.pop(number)
            break
    else:
        return None
    with open(DATABASE_FILENAME, mode='w', newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_fields)

    if deleted_task:
        dict_task_without_id = deleted_task.model_dump()
        del dict_task_without_id["id"]
        return Task(**dict_task_without_id)