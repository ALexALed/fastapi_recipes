from todo_app import operations
from todo_app.models import Task
from todo_app.operations import create_task

operations.DATABASE_FILENAME = 'test_tasks.csv'


def test_add_task():
    tasks = operations.read_all_tasks()
    assert len(tasks) == 0
    create_task(Task(title='test', description='test', status='done'))
    tasks = operations.read_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == 'test'
    assert tasks[0].description == 'test'
    assert tasks[0].status == 'done'

def test_get_next_id():
    tasks = operations.read_all_tasks()
    assert len(tasks) == 0
    create_task(Task(title='test', description='test', status='done'))
    create_task(Task(title='test', description='test', status='done'))
    assert operations.get_next_id() == 3

def test_read_task_by_id():
    tasks = operations.read_all_tasks()
    assert len(tasks) == 0
    create_task(Task(title='test1', description='test', status='done'))
    create_task(Task(title='test2', description='test', status='done'))
    assert operations.read_task_by_id(2).title == 'test2'

def test_modify_task():
    tasks = operations.read_all_tasks()
    assert len(tasks) == 0
    create_task(Task(title='test1', description='test', status='done'))
    create_task(Task(title='test2', description='test', status='done'))
    operations.modify_task(2, {"title":'test3'})
    task = operations.read_task_by_id(2)
    assert task.title == 'test3'

def test_remove_task():
    tasks = operations.read_all_tasks()
    assert len(tasks) == 0
    create_task(Task(title='test1', description='test', status='done'))
    operations.remove_task(1)
    tasks = operations.read_all_tasks()
    assert len(tasks) == 0

