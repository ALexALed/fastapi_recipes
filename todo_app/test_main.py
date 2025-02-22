from main import app

from fastapi.testclient import TestClient

from todo_app import operations
from todo_app.operations import read_all_tasks

client = TestClient(app)

operations.DATABASE_FILENAME = 'test_tasks.csv'


def test_read_all_tasks():
    operations.create_task(operations.Task(title='test1', description='test 1', status='done'))
    operations.create_task(operations.Task(title='test2', description='test 2', status='done'))
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == [{'description': 'test 1', 'id': 1, 'status': 'done', 'title': 'test1'},
                               {'description': 'test 2', 'id': 2, 'status': 'done', 'title': 'test2'}]


def test_endpoint_get_task():
    operations.create_task(operations.Task(title='test1', description='test 1', status='done'))
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json() == {'description': 'test 1', 'id': 1, 'status': 'done', 'title': 'test1'}
    response = client.get("/tasks/11")
    assert response.status_code == 404


def test_endpoint_create_task():
    task = {
        "title": "To Define",
        "description": "will be done",
        "status": "Ready",
    }
    response = client.post("/tasks", json=task)
    assert response.status_code == 200
    assert response.json() == {**task, "id": 1}
    assert len(read_all_tasks()) == 1


def test_endpoint_modify_task():
    operations.create_task(operations.Task(title='test1', description='test 1', status='done'))
    updated_fields = {"status": "Finished"}
    response = client.put("/tasks/1", json=updated_fields)
    assert response.status_code == 200
    assert response.json() == {
        **{'description': 'test 1', 'id': 1, 'status': 'done', 'title': 'test1'},
        **updated_fields,
    }
    response = client.put(
        "/task/3", json=updated_fields
    )
    assert response.status_code == 404

def test_endpoint_delete_task():
    operations.create_task(operations.Task(title='test1', description='test 1', status='done'))
    response = client.delete("/tasks/1")
    assert response.status_code == 200
    assert response.json() == {'title': 'test1', 'description': 'test 1', 'status': 'done'}
    assert len(read_all_tasks()) == 0