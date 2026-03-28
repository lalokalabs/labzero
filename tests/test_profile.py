import pytest
import json
from django.urls import reverse


pytestmark = pytest.mark.django_db


def test_profile_requires_login(client):
    response = client.get(reverse("labzero:profile"))

    assert response.status_code == 302
    assert response.url.startswith("/app/login/")


def test_profile_renders_inside_labzero_layout(authenticated_client):
    response = authenticated_client.get(reverse("labzero:profile"))
    html = response.content.decode()

    assert response.status_code == 200
    assert "Profile Settings" in html
    assert "LabZero" in html
    assert "Dashboard" in html
    assert 'name="name"' in html
    assert 'name="email"' in html
    assert 'name="new_password1"' in html
    assert "/static/django_umin/dist/" in html
    assert "/static/labzero/dist/" in html


def test_dashboard_sidebar_links_to_profile(authenticated_client):
    response = authenticated_client.get(reverse("labzero:dashboard"))
    html = response.content.decode()

    assert response.status_code == 200
    assert 'href="/app/profile/"' in html


def test_profile_updates_name_and_email(authenticated_client, user):
    response = authenticated_client.post(
        reverse("labzero:profile"),
        {
            "name": "Updated User",
            "email": "updated@example.com",
            "current_password": "",
            "new_password1": "",
            "new_password2": "",
        },
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    trigger = json.loads(response.headers["HX-Trigger"])
    assert trigger["labzero:notify"]["message"] == "Your profile was updated successfully."
    assert trigger["labzero:notify"]["type"] == "success"

    user.refresh_from_db()
    assert user.name == "Updated User"
    assert user.email == "updated@example.com"


def test_profile_updates_password_and_keeps_session(authenticated_client, user):
    response = authenticated_client.post(
        reverse("labzero:profile"),
        {
            "name": user.name,
            "email": user.email,
            "current_password": "InitialPass123!",
            "new_password1": "UpdatedPass123!",
            "new_password2": "UpdatedPass123!",
        },
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    trigger = json.loads(response.headers["HX-Trigger"])
    assert trigger["labzero:notify"]["message"] == "Your profile was updated successfully."

    user.refresh_from_db()
    assert user.check_password("UpdatedPass123!")

    follow_up = authenticated_client.get(reverse("labzero:profile"))
    assert follow_up.status_code == 200
