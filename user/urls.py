
from django.urls import path

from .views import *

urlpatterns = [
    path('signup/', RegisterUserAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('reset/', forgot_password_request),
    path('verify/request/', request_verification),
    path('verify/confirm/', confirm_verification),
    path('me/get/', get_current_account),
]
