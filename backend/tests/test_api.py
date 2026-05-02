import os
from datetime import datetime
os.environ['SKIP_DB_INIT'] = '1'

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.auth import get_password_hash
from app.database import Base, get_db
from app.main import app
from app.models import Movie, Theater, User

engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
API = '/api/v1'


@pytest.fixture(scope='module', autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    movie = Movie(
        title='Test Movie',
        description='Desc',
        genre='Action',
        duration=120,
        release_date=datetime(2023, 1, 1),
        poster_url='url',
    )
    theater = Theater(name='Test Theater', location='Location')
    db.add(movie)
    db.add(theater)
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def admin_user():
    db = TestingSessionLocal()
    existing = db.query(User).filter(User.email == 'admin@test.com').first()
    if existing:
        db.expunge(existing)
        db.close()
        return existing

    user = User(email='admin@test.com', hashed_password=get_password_hash('password'), role='admin')
    db.add(user)
    db.commit()
    db.refresh(user)
    db.expunge(user)
    db.close()
    return user


def test_register_user():
    response = client.post(f'{API}/auth/register', json={'email': 'test@example.com', 'password': 'password'})
    assert response.status_code == 200
    assert 'access_token' in response.json()


def test_register_ignores_client_role():
    response = client.post(f'{API}/auth/register', json={'email': 'safe@example.com', 'password': 'password', 'role': 'admin'})
    assert response.status_code == 200

    db = TestingSessionLocal()
    user = db.query(User).filter(User.email == 'safe@example.com').first()
    assert user.role == 'user'
    db.close()


def test_login_user():
    client.post(f'{API}/auth/register', json={'email': 'login@example.com', 'password': 'password'})
    response = client.post(f'{API}/auth/login', data={'username': 'login@example.com', 'password': 'password'})
    assert response.status_code == 200
    assert 'access_token' in response.json()


def test_get_movies():
    response = client.get(f'{API}/movies')
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_create_movie(admin_user):
    login_response = client.post(f'{API}/auth/login', data={'username': 'admin@test.com', 'password': 'password'})
    token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    movie_data = {
        'title': 'New Movie',
        'description': 'Test Description',
        'genre': 'Action',
        'duration': 120,
        'release_date': '2023-01-01T00:00:00',
        'poster_url': 'http://example.com/poster.jpg',
    }
    response = client.post(f'{API}/movies', json=movie_data, headers=headers)
    assert response.status_code == 200
    assert response.json()['title'] == 'New Movie'


def test_get_current_user(admin_user):
    login_response = client.post(f'{API}/auth/login', data={'username': 'admin@test.com', 'password': 'password'})
    token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    response = client.get(f'{API}/auth/me', headers=headers)
    assert response.status_code == 200
    assert response.json()['email'] == 'admin@test.com'
    assert response.json()['role'] == 'admin'


def test_update_movie(admin_user):
    login_response = client.post(f'{API}/auth/login', data={'username': 'admin@test.com', 'password': 'password'})
    token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    movie_data = {
        'title': 'Updated Movie',
        'description': 'Updated Description',
        'genre': 'Drama',
        'duration': 130,
        'release_date': '2024-02-01T00:00:00',
        'poster_url': '/posters/updated.svg',
    }
    response = client.put(f'{API}/movies/1', json=movie_data, headers=headers)
    assert response.status_code == 200
    assert response.json()['title'] == 'Updated Movie'


def test_delete_movie(admin_user):
    login_response = client.post(f'{API}/auth/login', data={'username': 'admin@test.com', 'password': 'password'})
    token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    movie_data = {
        'title': 'Delete Movie',
        'description': 'Delete Description',
        'genre': 'Action',
        'duration': 100,
        'release_date': '2024-03-01T00:00:00',
        'poster_url': '/posters/delete.svg',
    }
    create_response = client.post(f'{API}/movies', json=movie_data, headers=headers)
    movie_id = create_response.json()['id']

    response = client.delete(f'{API}/movies/{movie_id}', headers=headers)
    assert response.status_code == 200
    assert response.json()['message'] == 'Movie deleted successfully'


def test_create_theater(admin_user):
    login_response = client.post(f'{API}/auth/login', data={'username': 'admin@test.com', 'password': 'password'})
    token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    response = client.post(
        f'{API}/theaters',
        json={'name': 'Admin Theater', 'location': 'New District'},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()['name'] == 'Admin Theater'


def test_update_theater(admin_user):
    login_response = client.post(f'{API}/auth/login', data={'username': 'admin@test.com', 'password': 'password'})
    token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    response = client.put(
        f'{API}/theaters/1',
        json={'name': 'Updated Theater', 'location': 'Updated Location'},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()['name'] == 'Updated Theater'


def test_delete_theater(admin_user):
    login_response = client.post(f'{API}/auth/login', data={'username': 'admin@test.com', 'password': 'password'})
    token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    create_response = client.post(
        f'{API}/theaters',
        json={'name': 'Delete Theater', 'location': 'To Remove'},
        headers=headers,
    )
    theater_id = create_response.json()['id']

    response = client.delete(f'{API}/theaters/{theater_id}', headers=headers)
    assert response.status_code == 200
    assert response.json()['message'] == 'Theater deleted successfully'


def test_get_bookings():
    client.post(f'{API}/auth/register', json={'email': 'user@example.com', 'password': 'password'})
    login_response = client.post(f'{API}/auth/login', data={'username': 'user@example.com', 'password': 'password'})
    token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    response = client.get(f'{API}/bookings', headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_booking():
    client.post(f'{API}/auth/register', json={'email': 'booker@example.com', 'password': 'password'})
    login_response = client.post(f'{API}/auth/login', data={'username': 'booker@example.com', 'password': 'password'})
    token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    booking_data = {
        'movie_id': 1,
        'theater_id': 1,
        'show_time': '2023-01-01T20:00:00',
        'seats': ['A1', 'A2'],
    }
    response = client.post(f'{API}/bookings', json=booking_data, headers=headers)
    assert response.status_code == 200
    assert response.json()['seats'] == ['A1', 'A2']


def test_prevent_double_booking():
    client.post(f'{API}/auth/register', json={'email': 'double@example.com', 'password': 'password'})
    login_response = client.post(f'{API}/auth/login', data={'username': 'double@example.com', 'password': 'password'})
    token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    booking_data = {
        'movie_id': 1,
        'theater_id': 1,
        'show_time': '2023-01-01T20:00:00',
        'seats': ['A1'],
    }
    response = client.post(f'{API}/bookings', json=booking_data, headers=headers)
    assert response.status_code == 409
