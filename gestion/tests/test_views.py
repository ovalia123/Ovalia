import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from gestion.models import Sales, CartItem, Order

@pytest.mark.django_db
class TestEcommerceViews:

    def setup_method(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="12345")
        self.sale = Sales.objects.create(
            name="Bracelet Test",
            category="poignee",
            materiaux="Or massif 14k",
            available=True
        )

    def test_boutique_access(self, client):
        url = reverse("boutique")
        response = client.get(url)
        assert response.status_code == 200
        assert b"Bracelet" in response.content

    def test_add_to_cart(self, client):
        url = reverse("add_to_cart", args=[self.sale.id, "poignee"])
        response = client.get(url)
        assert response.status_code == 302  # redirect to cart

        # Vérifie que l'item est bien en base
        assert CartItem.objects.count() == 1
        item = CartItem.objects.first()
        assert item.sale == self.sale
        assert item.wear_type == "poignee"
        assert item.quantity == 1

    def test_cart_view(self, client):
        CartItem.objects.create(sale=self.sale, wear_type="poignee", quantity=2, user=None)
        response = client.get(reverse("cart"))
        assert response.status_code == 200

    def test_checkout_session(self, client, settings, monkeypatch):
        # Prépare l’environnement
        CartItem.objects.create(sale=self.sale, wear_type="poignee", quantity=1, user=None)

        # Mock Stripe pour éviter les vraies connexions
        class DummySession:
            id = "test-session-id"
        monkeypatch.setattr("stripe.checkout.Session.create", lambda *args, **kwargs: DummySession())

        settings.STRIPE_SECRET_KEY = "sk_test_xxx"
        settings.PAYMENT_SUCCESS_URL = "http://test/success/"
        settings.PAYMENT_CANCEL_URL = "http://test/cancel/"

        url = reverse("checkout")
        response = client.get(url)
        assert response.status_code == 200
        assert "sessionId" in response.json()
