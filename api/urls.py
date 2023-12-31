from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login,name='login'),
    path('register/',views.registration_view, name='register'),
    path('otp-verification/<int:user_id>/',views.otp_verification, name='otp_verification'),
    path('resend-otp/<int:user_id>/',views.resend_otp, name='resend_otp'),
    path('get-data/',views.get_data, name='get_data'),
]
