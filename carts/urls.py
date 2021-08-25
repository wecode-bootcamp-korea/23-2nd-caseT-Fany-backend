from django.urls import path

from carts.views import CustomProductView

urlpatterns = [
    path('/<int:product_id>/custom', CustomProductView.as_view()),
]