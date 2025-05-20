from django.urls import path
from .import views

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name='register'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('identifyuser/',views.identifyuserView.as_view(),name='identifyuser'),
    path('otpverification/<str:username>/',views.ValidateOTPView.as_view(),name='otp'),
    path('resetpassword/<str:username>/',views.PasswordResetView.as_view(),name='resetpassword'),
    path('home/',views.HomeView.as_view(),name='home'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
]