"""
URL configuration for tourist project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
'''
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import book_package, booking_success
# from .views import submit_enquiry
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    # Add more URL patterns as per your requirements
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('packages/', views.packages, name='packages'),
    path('package/<int:package_id>/', views.package_details, name='package_details'),
    path('destination/', views.destination, name='destination'),
    path('404/', views.error_404, name='error_404'),
    ######################################################
    # path('packages/', package_list, name='package_list'),
    # path('packages/<int:package_id>/', package_details, name='package_details'),
    path('packages/<int:package_id>/book/', book_package, name='book_package'),
    path('booking-success/', booking_success, name='booking_success'),
    ######################################################
    # path('register/', views.register, name='register'),
    # path('login/', views.login, name='login'),
    # path('logout/', views.logout, name='logout'),
    path('accounts/', include('accounts.urls')),
    path('enquiry/', include('enquiry.urls')),
    path('destination/', include('destination.urls')),
    # path("payment-success/", views.payment_success, name="payment_success"),
    path("payment-success/", views.payment_success, name="payment_success"),
    
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ✅ Home & Basic Pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('destination/', views.destination, name='destination'),
    path('404/', views.error_404, name='error_404'),

    # ✅ Packages (Tour Packages List & Details)
    path('packages/', views.packages, name='packages'),
    path('package/<int:package_id>/', views.package_details, name='package_details'),

    # ✅ Booking & Payments
    path('packages/<int:package_id>/book/', views.book_package, name='book_package'),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('booking-confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('booking-details/<int:booking_id>/', views.booking_show, name='booking_show'),
    path('booking-ticket/<int:booking_id>/', views.generate_ticket_pdf, name='booking_ticket'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('all-bookings/', views.all_bookings, name='all_bookings'),
    path('my-bookings/', views.user_bookings, name='user_bookings'),

    


    # ✅ Accounts & Authentication
    path('accounts/', include('accounts.urls')),
    path('profile/', views.profile_view, name='profile'),
    

    # ✅ Other Apps
    path('enquiry/', include('enquiry.urls')),
    path('destination/', include('destination.urls')),

    # Other models
    path("", include("team.urls")),

]

# ✅ Media files handling in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
