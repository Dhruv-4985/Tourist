from django.db import models

class Enquiry(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    datetime = models.CharField(max_length=100)  # You can use DateTimeField if needed
    destination = models.CharField(max_length=255)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Enquiry from {self.name} - {self.email}"
