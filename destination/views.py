from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Destination

def home(request):
    destinations = Destination.objects.all()
    return render(request, "index.html", {"destinations": destinations})
