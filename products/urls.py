from django.urls import path

from products.views import Productview

urlpatterns = [
    path('', Productview.as_view()),
]