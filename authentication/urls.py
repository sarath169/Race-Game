from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.RegistrationView.as_view(), name = "signup"),
    path('login/', views.LoginView.as_view(), name = "login" ),
    path('logout/', views.LogoutView.as_view(), name = "logout" ),
    path('changepassword/', views.PasswordChangeView.as_view(), name = "change_password"),
    path('sendotp/', views.SendMailView.as_view(), name = "send otp"),
    path('forgotpassword/', views.ForgotPasswordView.as_view(), name = "forgot_password"),
    path('verifyotp/', views.VerifyOtpView.as_view(), name = "verify_otp"),
]
