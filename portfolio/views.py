from django.shortcuts import render, redirect
from .models import *

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages

from .custom_email import *

# Create your views here.
def index(request):
    var = {
        'nbar': 'home'
    }
    return render(request, 'home/index.html',var)

def about_us(request):
    var = {
        'nbar': 'aboutus'
    }
    return render(request , 'other/about.html',var)

def services(request):
    var = {
        'nbar': 'services'
    }
    return render(request , 'other/services.html',var)

def contact_us_page(request):
    var = {
        'nbar': 'contact'
    }
    return render(request , 'other/contact.html',var)

def submit_contact_form(request):
    if request.method == 'POST':
        name = request.POST['name']
        number = request.POST['number']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        # print(name,number,email,subject,message)
        try:
            form_data = contact_us.objects.create(name=name,email=email,phone=number,subject=subject,message=message)
            form_data.save()
            send = send_custom_email_to_admins(name,number,email,subject,message)
            messages.success(request, "We've receive your response. We'll soon in touch with you.")
            return redirect('contact-us')
        except:
            messages.error(request, "Something wents wrong. Please try again.")
            return redirect('contact-us')

def handler404(request, exception):
    return render(request, 'error/404.html')

def handler403(request, exception):
    return render(request, 'error/403.html')

def handler500(request):
    return render(request, 'error/500.html')
