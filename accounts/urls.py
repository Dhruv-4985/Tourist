from accounts import views
from django.urls import path

urlpatterns = [
    path('register/', views.register, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
]