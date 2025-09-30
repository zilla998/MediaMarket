import pytest
from django.urls import reverse

from fixtures.conftest import auth_client, product

@pytest.mark.django_db
class TestProductURLs:
    @pytest.mark.parametrize("url,expected_status", [
        (reverse("products:homepage"), 200),
        (reverse("products:about_us"), 200),
        (reverse("products:products_list"), 200),
        (reverse("products:category_sort"), 200),
        (reverse("products:category_filter"), 200),
        (reverse("products:product_cart"), 200),
        # (reverse("products:product_checkout"), 405),
        # (reverse("products:users_order"), 405),
    ])
    def test_public_urls(self, client, url, expected_status):
        response = client.get(url)
        assert response.status_code == expected_status

    @pytest.mark.parametrize('url', [
        (reverse("products:favorite_product")),
        (reverse("products:add_product_to_favorite", kwargs={"pk": 1}))
    ])
    def test_protected_urls_redirect_anonymous(self, client, url):
        """Защищенные URL редиректят неавторизованных"""
        response = client.get(url)
        assert response.status_code == 302
        assert reverse("users:login") in response.url

    def test_protected_urls_allow_authenticated_favorite(self, auth_client, product):
        response = auth_client.get(reverse("products:favorite_product"))
        assert response.status_code == 200
        response = auth_client.get(
            reverse("products:add_product_to_favorite", kwargs={"pk": product.pk})
        )
        assert response.status_code == 302
