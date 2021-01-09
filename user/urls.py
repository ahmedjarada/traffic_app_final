from django.urls import path
from Auth.knox_view import LogoutView
from .views import *

urlpatterns = [
    path('signup/', RegisterUserAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', LogoutView.as_view()),
    path('reset/request', forgot_password_request),
    path('reset/confirm/', forgot_password_confirm),
    path('reset/check/', forgot_password_check_pin),
    path('verify/request/', request_verification),
    path('verify/confirm/', confirm_verification),
    path('me/get/', get_current_account),
]
