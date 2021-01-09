from django.urls import path
from .views import *

urlpatterns = [
    path('add/', add),
    path('list/', ls),
    path('delete/', delete)
]
