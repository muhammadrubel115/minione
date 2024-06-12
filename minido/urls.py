from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# all imoprt for urls are here

from django.urls import path
from minido import views

# Write urls for minigen here !!

urlpatterns = [
    path('', views.about, name="about"),
    path('privacy_policy/', views.PrivacyPolicy, name="privacy_policy"),
    path('terms_and_conditions/', views.TermsAndConditions, name="terms_and_conditions"),
    path('cookies/', views.Cookies, name="cookies"),
    path('faq/', views.Faq, name="faq"),
    path('developers/', views.Developers, name="developers"),


]