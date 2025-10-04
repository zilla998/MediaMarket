from django.urls import reverse

import pytest
from fixtures.conftest import custom_user_factory


def test_urls_no_auth(db, client, custom_user_factory):
    user = custom_user_factory()

    url_no_params = {
        reverse("users:login"): 200,
        reverse("users:register"): 200,
        reverse("users:logout"): 405,
        reverse("users:user_profile_settings"): 302,
    }
    url_params = {
        reverse("users:user_profile", kwargs={"pk": user.pk}): 302,
        reverse("users:user_profile_orders", kwargs={"pk": user.pk}): 302,
    }

    for url, status_code in url_no_params.items():
        response = client.get(url)

        assert response.status_code == status_code

    for url, status_code in url_params.items():
        response = client.get(url)

        assert response.status_code == status_code


def test_urls_auth(db, client, custom_user_factory):
    user = custom_user_factory()
    client.force_login(user)

    url_no_params = {
        reverse("users:login"): 200,
        reverse("users:register"): 200,
        reverse("users:logout"): 405,
        reverse("users:user_profile_settings"): 200,
    }
    url_params = {
        reverse("users:user_profile", kwargs={"pk": user.pk}): 200,
        reverse("users:user_profile_orders", kwargs={"pk": user.pk}): 200,
    }

    for url, status_code in url_no_params.items():
        response = client.get(url)
        assert response.status_code == status_code

    for url, status_code in url_params.items():
        response = client.get(url)
        assert response.status_code == status_code
