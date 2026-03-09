"""Root pytest configuration — shared fixtures for all tests."""
import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """Unauthenticated DRF test client."""
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, django_user_model):
    """DRF test client force-authenticated as a regular user."""
    user = django_user_model.objects.create_user(username="testuser", password="testpass")
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_client(api_client, django_user_model):
    """DRF test client force-authenticated as a staff/superuser."""
    user = django_user_model.objects.create_superuser(
        username="admin", password="adminpass", email="admin@example.com"
    )
    api_client.force_authenticate(user=user)
    return api_client
