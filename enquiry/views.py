from django.shortcuts import render, redirect
from .forms import EnquiryForm
from django.contrib import messages

def submit_enquiry(request):
    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your enquiry has been submitted successfully!")
            return redirect('home')  # Change 'home' to the correct redirect page
        else:
            messages.error(request, "There was an error. Please try again.")

    else:
        form = EnquiryForm()

    return render(request, 'index.html', {'form': form})
