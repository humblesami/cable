from django.urls import path
from noman.views import index, million_areas, get_due_amount, get_subscription_charges

urlpatterns = [
    path('', index),
    path('subscription/charges', get_subscription_charges),
    path('sale_object/charges', get_due_amount),
    path('million/area', million_areas),
]
