import json
import pytest
from app.models.models import db, User, Task
from main import init_app

@pytest.fixture(scope='module')
def test_client():
    app = init_app()
    app.config.from_object('test.test_config.TestConfig')
    
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()

@pytest.fixture(scope='module')
def new_user(test_client):
    test_client.post('/api/user/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })

@pytest.fixture(scope='module')
def login_token(test_client, new_user):
    response = test_client.post('/api/user/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    token = response.get_json()['access_token']
    return token


def test_register(test_client):
    response = test_client.post('/api/user/register', json={
        'username': 'anotheruser',
        'password': 'anotherpassword'
    })
    data = response.get_json()
    assert response.status_code == 201
    assert data['message'] == 'User created successfully'

def test_register_existing_user(test_client, new_user):
    response = test_client.post('/api/user/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    data = response.get_json()
    assert response.status_code == 400
    assert data['message'] == 'User already exists'

def test_register_missing_key(test_client, new_user):
    response = test_client.post('/api/user/register', json={
        'username': 'testuser'
    })
    data = response.get_json()
    assert response.status_code == 400
    assert data['message'] == 'Username and password required'

def test_login(test_client, new_user):
    response = test_client.post('/api/user/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert 'access_token' in data

def test_login_fail(test_client, new_user):
    response = test_client.post('/api/user/login', json={
        'username': 'testuser1',
        'password': 'testpassword'
    })
    data = response.get_json()
    assert response.status_code == 401

def test_register_missing_key(test_client, new_user):
    response = test_client.post('/api/user/login', json={
        'username': 'testuser'
    })
    data = response.get_json()
    assert response.status_code == 400
    assert data['message'] == 'Username and password required'

def test_create_task(test_client, login_token):
    response = test_client.post('/api/todo/tasks', headers={
        'Authorization': f'Bearer {login_token}'
    }, json={
        'title': 'Test Task',
        'description': 'Test Description',
        'completed': True
    })
    data = response.get_json()
    assert response.status_code == 201
    assert data['message'] == 'Task created successfully'

def test_get_tasks(test_client, login_token):
    response = test_client.get('/api/todo/tasks', headers={
        'Authorization': f'Bearer {login_token}'
    })
    data = response.get_json()
    print(data)
    assert response.status_code == 200
    assert len(data) > 0

def test_update_task(test_client, login_token):
    response = test_client.get('/api/todo/tasks', headers={
        'Authorization': f'Bearer {login_token}'
    })
    data = response.get_json()
    task_id = data[0]['id']
    
    # Update the task
    response = test_client.put(f'/api/todo/tasks/{task_id}', headers={
        'Authorization': f'Bearer {login_token}'
    }, json={
        'title': 'Updated Task',
        'description': 'Updated Description'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data['message'] == 'Task updated successfully'

def test_delete_task(test_client, login_token):
    response = test_client.get('/api/todo/tasks', headers={
        'Authorization': f'Bearer {login_token}'
    })
    data = response.get_json()
    task_id = data[0]['id']
    # Delete the task
    response = test_client.delete(f'/api/todo/tasks/{task_id}', headers={
        'Authorization': f'Bearer {login_token}'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data['message'] == 'Task deleted successfully'
