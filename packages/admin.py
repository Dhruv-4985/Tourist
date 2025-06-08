from django.contrib import admin

# Register your models here.

from .models import Package

class PackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'tour_type', 'price', 'rating')
    search_fields = ('title', 'location', 'tour_type')
    list_filter = ('tour_type',)

admin.site.register(Package, PackageAdmin)

from django.contrib import admin
from .models import Package,Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "user_email", "package", "amount", "payment_id", "created_at")
    search_fields = ("order_id", "user_email", "payment_id")
    list_filter = ("created_at",)
    ordering = ("-created_at",)  # Show latest bookings first


# from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'package', 'booking_date', 'total_amount', 'payment_status')
    search_fields = ('full_name', 'email')
    list_filter = ('payment_status', 'booking_date')
