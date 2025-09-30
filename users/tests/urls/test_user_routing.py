from django.urls import reverse

from fixtures.conftest import user


def test_urls_no_auth(db, client, user):
    url_no_params = {
        reverse("users:login"): 200,
        reverse("users:register"): 200,
        # reverse("users:recover-password"): 200,
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


def test_urls_auth(db, client, user):
    client.force_login(user)
    pass
