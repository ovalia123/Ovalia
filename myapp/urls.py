from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('member/', views.member, name='member'),
    path('faq/', views.faq, name='faq'),
    path('event/', views.event, name='event'),
    path('service/', views.service, name='service'),
    path('condition/', views.condition, name='condition'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.cart, name='cart'),

    # shop
    path('shop/', views.shop, name='shop'),
    path('shop/or14k', views.shop_14k, name='or14k'),
    path('shop/or10k', views.shop_10k, name='or10k'),
    path('shop/argent', views.shop_argent, name='argent'),
    path('shop/orRempli', views.shop_rempli, name='orrempli'),
    path('shop/charms', views.charms, name='charms'),

    # boutique & ecommerce
    path('boutique/', views.boutique, name='boutique'),
    path('boutique/<int:sale_id>/', views.sale_detail, name='sale_detail'),
    path('boutique/<int:sale_id>/ajouter/', views.add_to_cart, name='add_to_cart'),
    path('boutique/<int:sale_id>/mise-a-jour/', views.update_cart, name='update_cart'),
    path('boutique/<int:sale_id>/supprimer/', views.remove_from_cart, name='remove_from_cart'),

    path("checkout/", views.checkout, name="checkout"),
    path("checkout/create/", views.create_checkout_session, name="create-checkout-session"),
    path("checkout/success/", views.checkout_success, name="checkout_success"),
    path("checkout/cancel/", views.checkout_cancel, name="checkout_cancel"),
    path("stripe/webhook/", views.stripe_webhook, name="stripe-webhook"),

]
