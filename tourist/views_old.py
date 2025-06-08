from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import razorpay

# Import models
from packages.models import Package, Booking, Order
from destination.models import Destination
from services.models import Service

# Import forms
from packages.forms import PackageSearchForm, BookingForm

def home(request):
    services = Service.objects.all()
    packages = Package.objects.all()
    destinations = Destination.objects.all()
    return render(request, 'index.html', {'services': services, 'packages': packages, 'destinations': destinations})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def services(request):
    services = Service.objects.all()
    return render(request, 'service.html', {'services': services})

def packages(request):
    packages = Package.objects.all()
    form = PackageSearchForm(request.GET)
    if form.is_valid():
        location = form.cleaned_data.get("location")
        min_price = form.cleaned_data.get("min_price")
        max_price = form.cleaned_data.get("max_price")
        min_duration = form.cleaned_data.get("min_duration")
        if location:
            packages = packages.filter(location__icontains=location)
        if min_price:
            packages = packages.filter(price__gte=min_price)
        if max_price:
            packages = packages.filter(price__lte=max_price)
        if min_duration:
            packages = packages.filter(duration__gte=min_duration)
    return render(request, "package.html", {"packages": packages, "form": form})

def package_details(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    return render(request, "package_details.html", {"package": package})

@login_required
def book_package(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        booking_date = request.POST.get("booking_date")
        no_of_people = int(request.POST.get("no_of_people"))
        total_amount = package.price * no_of_people
        request.session["email"] = email
        request.session["package_id"] = package.id
        request.session.modified = True
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        order_data = {"amount": int(total_amount * 100), "currency": "INR", "payment_capture": "1"}
        order = client.order.create(data=order_data)
        booking = Booking.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            booking_date=booking_date,
            no_of_people=no_of_people,
            total_amount=total_amount,
            razorpay_order_id=order["id"],
            package=package,
        )
        return render(request, "payment_page.html", {
            "package": package,
            "total_amount": total_amount,
            "order_id": order["id"],
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "booking": booking
        })
    return render(request, "booking.html", {"package": package})

def create_order(request):
    amount = int(request.POST.get("razorpay_amount"))
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    order = client.order.create({"amount": amount, "currency": "INR", "payment_capture": "1"})
    return JsonResponse(order)

def payment_success(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            payment_id = data.get("razorpay_payment_id")
            email = request.session.get("email")
            package_id = request.session.get("package_id")
            if not email or not package_id:
                return JsonResponse({"status": "error", "message": "Session expired or missing!"})
            package = get_object_or_404(Package, id=package_id)
            order = Order.objects.create(
                user_email=email,
                package=package,
                order_id=f"ORD{package_id}{payment_id[-6:]}",
                payment_id=payment_id,
                amount=package.price
            )
            del request.session["email"]
            del request.session["package_id"]
            request.session.modified = True
            return JsonResponse({
                "status": "success",
                "message": "Payment successful! Order saved.",
                "order_id": order.order_id
            })
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

def booking_success(request):
    return render(request, 'booking_success.html')

def destination(request):
    return render(request, 'destination.html')

def error_404(request, exception):
    return render(request, '404.html')

def initiate_payment(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    return render(request, "payment.html", {
        "package": package,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": int(package.price * 100)
    })
