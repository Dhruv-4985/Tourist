from django.urls import path
from .views import submit_enquiry

urlpatterns = [
    path('submit-enquiry/', submit_enquiry, name='submit_enquiry'),
]
