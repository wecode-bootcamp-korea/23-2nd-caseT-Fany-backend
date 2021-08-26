from django.urls import path

from reviews.views import ReviewView

urlpatterns = [
    path('/<int:product_id>/review',ReviewView.as_view()),
    path('/<int:product_id>/review/<int:review_id>',ReviewView.as_view()),
]