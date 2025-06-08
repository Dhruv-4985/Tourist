from django.db import models

# Create your models here.

class service(models.Model):
    icon = models.CharField(max_length=50,help_text="FontAwesome v4 icons are supported. Example: fa fa-home")
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=70)