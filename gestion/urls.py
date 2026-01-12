from django.urls import path

from . import views

urlpatterns = [
    #user panel
    path("admin/", views.admin, name="admin"),
    path('logout/',views.logout_view ,name='logout'),
    path('login/',views.login_view ,name='login'),
    path('register/',views.register_view ,name='register'),
    path('verify_user/<int:user_id>/', views.verify_user, name='verify_user'),
    

    #product panel
    path("product/", views.product, name="product"),
    path('product/add/', views.add_product, name='add_product'),
    path('product/<int:id>/edit/', views.edit_product, name='update_product'),
    path('product/<int:id>/delete/', views.delete_product, name='delete_product'),
    path('available/<int:product_id>/', views.available, name='available'),
]