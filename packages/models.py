
from django.db import models
from django.contrib.auth.models import User

# ✅ Package Model
class Package(models.Model):
    TOUR_TYPES = [
        ("Adventure", "Adventure"),
        ("Family", "Family"),
        ("Honeymoon", "Honeymoon"),
        ("Beach", "Beach"),
        ("Cultural", "Cultural"),
        ("Wildlife", "Wildlife"),
    ]
    title = models.CharField(max_length=200)  # Package title
    image = models.ImageField(upload_to='packages/images/')  # Package image
    location = models.CharField(max_length=100)  # Location name
    duration = models.CharField(max_length=50)  # Duration (e.g., "3 days")
    persons = models.IntegerField()  # Number of persons
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price in USD
    rating = models.FloatField(default=5.0)  # Rating (out of 5)
    description = models.TextField()  # Package description
    location_map = models.TextField()  # Google Map iframe src
    inclusions = models.TextField(default="Includes basic amenities.")
    tour_type = models.CharField(max_length=50, choices=TOUR_TYPES, default="Adventure")  # New Field

    def __str__(self):
        return self.title


# ✅ Booking Model
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    booking_date = models.DateField()
    no_of_people = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Total price
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)  # Razorpay order ID
    payment_status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Completed", "Completed")],
        default="Pending"
    )

    def save(self, *args, **kwargs):
        if self.package and self.no_of_people:
            self.total_amount = self.package.price * self.no_of_people
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking by {self.full_name} for {self.package.title}"


# ✅ Order Model
class Order(models.Model):
    order_id = models.CharField(max_length=20, unique=True)
    user_email = models.EmailField()
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} - {self.package.title}"
