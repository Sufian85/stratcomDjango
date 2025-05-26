from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home_view"),
    path("products", views.products_view, name="products_view"),
    path("products/<int:id>", views.product_detail_view, name="product_detail_view"),
    path("create-order", views.create_order, name="create_order"),
    path("order-details/<slug:orderId>", views.get_order_info, name="get-details"),
    path("orders", views.get_all_orders, name="get-all-orders")
]