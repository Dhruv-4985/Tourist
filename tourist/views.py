from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#app models for import
from packages.models import Package,Booking
from destination.models import Destination
from team.models import TeamMember
# form are imported here
from packages.forms import PackageSearchForm,BookingForm

def home(request):
    services = service.objects.all()
    packages = Package.objects.all()
    team = TeamMember.objects.all()
    destinations = Destination.objects.all()
    return render(request, 'index.html', {'services': services,'packages': packages,'destinations': destinations,'team':team})

def about(request):
    team = TeamMember.objects.all()
    return render(request, 'about.html',{'team': team})

def contact(request):
    return render(request, 'contact.html')

from services.models import service
def services(request):
    services = service.objects.all()
    return render(request, 'service.html', {'services': services})
    # return render(request, 'service.html')

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
    package = Package.objects.get(id=package_id)
    suggested_packages = Package.objects.filter(tour_type=package.tour_type).exclude(id=package.id)[:4]  # Show only 4 suggestions

    return render(request, "package_details.html", {
        "package": package,
        "suggested_packages": suggested_packages,
    })
    # return render(request, 'package_detail.html')

import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from packages.models import Booking, Package
from django.contrib.auth.decorators import login_required

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

        if email and package.id:
            request.session["email"] = email
            request.session["package_id"] = package.id
            request.session.modified = True  # Force session save
            print("Session Set:", request.session.get("email"), request.session.get("package_id"))
        else:
            print("❌ Error: Email or Package ID Missing")

        order_data = {
            "amount": int(total_amount * 100),  # Razorpay requires amount in paise
            "currency": "INR",
            "payment_capture": "1",
        }
        order = client.order.create(data=order_data)

        booking = Booking.objects.create(
            user=request.user,
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

# import razorpay
from django.conf import settings

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def create_order(request):
    amount = int(request.POST.get("razorpay_amount"))  # Amount in paise
    order = client.order.create({"amount": amount, "currency": "INR", "payment_capture": "1"})
    return JsonResponse(order)



import json
from django.shortcuts import get_object_or_404
from packages.models import Package, Order

def payment_success(request):
    """Handle successful payments and save order details"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Read JSON data from request
            payment_id = data.get("razorpay_payment_id")
            print("Received Payment Data:", data)  # Debugging Log

            # ✅ Retrieve session data
            email = request.session.get("email")
            package_id = request.session.get("package_id")
            print("Session Data Retrieved: Email:", email, "Package ID:", package_id)  # Debugging Log

            if not payment_id:
                print("❌ Payment ID is missing from Razorpay response")
                return JsonResponse({
                    "status": "error",
                    "message": "Payment ID is missing! Please contact support."
                })
            else:
                print("✅ Payment ID Received:", payment_id)

            if not email or not package_id:
                print("❌ ERROR: Session data missing!")
                return JsonResponse({"status": "error", "message": "Session expired or missing!"})

            package = get_object_or_404(Package, id=package_id)

            try:
                order = Order.objects.create(
                    user_email=email,
                    package=package,
                    # order_id=f"ORD{package_id}{payment_id[-6:]}",
                    order_id = f"ORD{package_id}{payment_id[-6:]}" if len(payment_id) >= 6 else f"ORD{package_id}{payment_id}",
                    payment_id=payment_id,
                    amount=package.price
                )
                print("✅ Order saved successfully:", order)

            except Exception as db_error:
                print("❌ ERROR: Database issue while saving order:", db_error)
                return JsonResponse({"status": "error", "message": f"Database error: {db_error}"})

            # ✅ Clear session after successful payment
            del request.session["email"]
            del request.session["package_id"]
            request.session.modified = True

            return JsonResponse({
                "status": "success",
                "message": "Payment successful! Order saved.",
                "order_id": order.order_id
            })

        except Exception as e:
            print("❌ ERROR: Unexpected issue in payment_success view:", e)
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

    return redirect("booking_show", booking_id=booking.id)


def booking_confirmation(request):
    """Show booking confirmation page after payment success"""
    order_id = request.GET.get("order_id")
    if order_id:
        return render(request, "booking_confirmation.html", {"order_id": order_id})
    else:
        return redirect("home")


# Booking Success Page
def booking_success(request):
    return render(request, 'booking_success.html')

def destination(request):
    return render(request, 'destination.html')

def error_404(request, exception):
    return render(request, '404.html')


###################################################################################
from django.http import JsonResponse
from packages.models import Package, Order

from django.conf import settings
from django.shortcuts import render
from packages.models import Package,Order
def initiate_payment(request, package_id):
    package = Package.objects.get(id=package_id)
    
    return render(request, "payment.html", {
        "package": package,
        "razorpay_key": settings.RAZORPAY_KEY_ID,  # Pass key from settings.py
        "amount": int(package.price * 100)  # Convert to paisa (required by Razorpay)
    })


from packages.models import Booking

def booking_show(request, booking_id):
    """Show Booking Confirmation with Ticket Details"""
    booking = get_object_or_404(Booking, id=booking_id)

    return render(request, "booking_details.html", {
        "booking": booking
    })

@login_required
def all_bookings(request):
    bookings = Booking.objects.all()
    return render(request, "all_bookings.html", {"bookings": bookings})


from django.contrib.auth.decorators import login_required
from packages.models import Booking

@login_required
def user_bookings(request):
    bookings = Booking.objects.filter(user=request.user)  # Only user's bookings
    return render(request, "user_bookings.html", {"bookings": bookings})

import reportlab
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


def generate_ticket_pdf(request, booking_id):
    """Generate PDF Ticket with Attractive Design"""
    booking = get_object_or_404(Booking, id=booking_id)

    # Create PDF Response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Ticket_{booking.id}.pdf"'

    # PDF Document
    pdf = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Custom Title Style
    title_style = ParagraphStyle('Title', parent=styles['Title'], fontSize=28, textColor=colors.HexColor("#333399"), alignment=1)
    elements.append(Paragraph("Travel Package Ticket Confirmation", title_style))
    elements.append(Spacer(1, 20))

    # Booking Details Table
    data = [
        ["Booking ID:", str(booking.id)],
        ["Name:", booking.full_name],
        ["Email:", booking.email],
        ["Phone:", booking.phone],
        ["Package:", booking.package.title],
        ["Date:", str(booking.booking_date)],
        ["Number of People:", str(booking.no_of_people)],
        ["Total Amount:", f"Rs{booking.total_amount}"],
        ["Payment Status:", booking.payment_status]
    ]

    table = Table(data, colWidths=[150, 300])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # Footer
    footer = Paragraph("Thank You for Booking with Us! <br/> Have a Safe Journey ✈️", styles['Italic'])
    elements.append(footer)

    # Build PDF
    pdf.build(elements)
    return response



@login_required
def profile_view(request):
    user = request.user
    bookings = Booking.objects.filter(user=user)  # Fetch bookings for the logged-in user
    return render(request, 'profile.html', {'user': user, 'bookings': bookings})
