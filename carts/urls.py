from django.urls import path

from carts.views import CustomProductView, CartView

urlpatterns = [
    path('', CartView.as_view()),
    path('/carts/<int:cart_id>', CartView.as_view()),
    path('/<int:product_id>/custom', CustomProductView.as_view()),
]