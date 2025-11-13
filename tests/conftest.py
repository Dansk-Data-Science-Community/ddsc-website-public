"""Pytest configuration and fixtures for DDSC"""
import pytest
from django.contrib.auth.models import User
from django.test import Client
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

# Markers
def pytest_configure(config):
    config.addinivalue_line("markers", "unit: unit tests")
    config.addinivalue_line("markers", "integration: integration tests")
    config.addinivalue_line("markers", "api: API endpoint tests")
    config.addinivalue_line("markers", "slow: slow tests")

# Django fixtures
@pytest.fixture
def db_setup(db):
    """Database setup fixture"""
    return db

@pytest.fixture
def user_factory(db):
    """Factory for creating test users"""
    def create_user(username="testuser", email="test@test.com", password="pass123", **kwargs):
        return User.objects.create_user(username=username, email=email, password=password, **kwargs)
    return create_user

@pytest.fixture
def admin_user_factory(db):
    """Factory for creating admin users"""
    def create_admin(username="admin", email="admin@test.com", password="pass123"):
        return User.objects.create_superuser(username=username, email=email, password=password)
    return create_admin

@pytest.fixture
def test_user(user_factory):
    """Standard test user"""
    return user_factory()

@pytest.fixture
def test_admin(admin_user_factory):
    """Standard admin user"""
    return admin_user_factory()

@pytest.fixture
def authenticated_user(test_user):
    """User with token"""
    token, _ = Token.objects.get_or_create(user=test_user)
    return test_user, token

# Client fixtures
@pytest.fixture
def client():
    """Django test client"""
    return Client()

@pytest.fixture
def api_client():
    """DRF API client"""
    return APIClient()

@pytest.fixture
def authenticated_api_client(authenticated_user):
    """Authenticated API client"""
    user, token = authenticated_user
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.key}')
    return client

# Data fixtures
@pytest.fixture
def sample_data(db, user_factory):
    """Sample data for tests"""
    return {
        'users': [user_factory(username=f'user{i}') for i in range(3)],
        'admin': user_factory(username='admin', is_staff=True, is_superuser=True),
    }

@pytest.fixture
def mock_request():
    """Mock HTTP request object"""
    class MockRequest:
        META = {
            'HTTP_USER_AGENT': 'TestClient',
            'HTTP_X_DEVICE_TYPE': 'test',
            'HTTP_X_APP_VERSION': '1.0',
        }
    return MockRequest()
