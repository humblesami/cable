from django.urls import path
from noman.views import index, million_areas, get_due_amount

urlpatterns = [
    path('', index),
    path('subscription/get_due_amount', get_due_amount),
    path('million/area', million_areas),
]
