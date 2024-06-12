

# all import of views are here

from django.shortcuts import render, redirect 
from django.http import HttpResponse
from datetime import datetime
from django.contrib import messages

# Models are imported
from minido.models import FAQ
# Create your views here.

def about(request):

    return render(request, 'minido/about.html')

def PrivacyPolicy(request):

    return render(request, 'minido/privacy_policy.html')

def TermsAndConditions(request):

    return render(request, 'minido/terms_and_conditions.html')

def Cookies(request):

    return render(request, 'minido/cookies.html')

def Faq(request):
    if request.method == 'POST':
        
        fullname = request.POST['fullname']
        email  = request.POST['email']
        faqbody   = request.POST['faqbody']


        myfaq = FAQ (fullname=fullname, email=email, faqbody=faqbody, date=datetime.today())
        myfaq.save()
        messages.success(request, "Your message has sent")
        
    return render(request, 'minido/faq.html')

def Developers(request):

    return render(request, 'minido/developers.html')