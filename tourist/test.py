from django.shortcuts import render, redirect
from django.contrib import messages

def verify_otp(request):
    if request.method == "POST":
        # Get the OTP input from the form
        digit1 = request.POST.get("digit1", "")
        digit2 = request.POST.get("digit2", "")
        digit3 = request.POST.get("digit3", "")
        digit4 = request.POST.get("digit4", "")
        
        # Combine digits into a full OTP code
        entered_otp = f"{digit1}{digit2}{digit3}{digit4}"

        # Assuming we stored the OTP in session during sending
        stored_otp = request.session.get("otp_code")

        if entered_otp == stored_otp:
            messages.success(request, "OTP Verified Successfully!")
            return redirect("dashboard")  # Redirect to a dashboard or homepage
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect("verify_otp")  # Reload OTP page with an error message

    return render(request, "verify_otp.html")

    import random
    from django.core.mail import send_mail
    
    def generate_otp():
        return str(random.randint(1000, 9999))
    
    def send_otp_email(request, user_email):
        otp_code = generate_otp()
        request.session["otp_code"] = otp_code  # Store OTP in session
        
        subject = "Your OTP Code"
        message = f"Your verification code is: {otp_code}"
        
        send_mail(subject, message, "your_email@example.com", [user_email])
    