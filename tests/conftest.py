import pytest


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        email="user@example.com",
        password="InitialPass123!",
        name="Initial User",
    )


@pytest.fixture
def authenticated_client(client, user):
    client.force_login(user)
    return client
