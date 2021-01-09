from django.urls import path
from Auth.knox_view import LogoutView
from .views import *

urlpatterns = [
    path('signup/', RegisterUserAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', LogoutView.as_view()),
    path('reset/', forgot_password_request),
    path('verify/request/', request_verification),
    path('verify/confirm/', confirm_verification),
    path('me/get/', get_current_account),
]
