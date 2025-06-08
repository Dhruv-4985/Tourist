from django.contrib import admin
from .models import Enquiry

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'destination', 'created_at')
    search_fields = ('name', 'email', 'destination')
    list_filter = ('destination', 'created_at')
