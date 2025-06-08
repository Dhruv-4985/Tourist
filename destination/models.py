from django.db import models

# Create your models here.


class Destination(models.Model):
    title = models.CharField(max_length=255)
    discount = models.CharField(max_length=10, help_text="Example: 30% OFF")
    image = models.ImageField(upload_to="destinations/")
    
    def __str__(self):
        return self.title
