from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('productos/', views.productos, name='productos'),
    path('productos/<slug:slug>/', views.producto_detalle, name='producto_detalle'),
    path('servicios/', views.servicios, name='servicios'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('contacto/', views.contacto, name='contacto'),
    # Carrito de compras
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/checkout/", views.checkout, name="checkout"),
    path("cart/increase/<int:product_id>/", views.increase_quantity, name="increase_quantity"),
    path("cart/decrease/<int:product_id>/", views.decrease_quantity, name="decrease_quantity"),
]