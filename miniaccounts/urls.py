from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from miniaccounts import views 


from django.urls import path
from miniaccounts.views import Register, verify_email

# URL patterns for miniaccounts app
from django.urls import path
from miniaccounts import views

urlpatterns = [
    path('', views.Register, name="register"),
    path('signin/', views.SignIn, name="signin"),
    path('verify-email/<uuid:token>/', views.verify_email, name='verify_email'),
    path('forgot_email/', views.ForgotEmail, name="forgot_email"),
    path('forgot_password/', views.ForgotPassword, name="forgot_password"),
    path('reset_password/<uidb64>/<token>/', views.ResetPassword, name='reset_password'),
]

# Serve static files during development
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

