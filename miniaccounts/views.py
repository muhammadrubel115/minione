from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# chatgpt results are here !!!

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


# varify email
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import EmailVerification
import uuid


# varification view
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages




# Views for user registration and authentication
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from miniaccounts.models import ProfileInfo
from django.core.mail import send_mail


def Register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        email = email.lower()

        if password != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Enter a valid email address")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')
        else:
            # Create user
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.is_active = False  # Deactivate the user until email verification
                user.save()

                # Create profile info
                profile = ProfileInfo.objects.create(user=user)
                profile.save()

                # Send verification email
                send_verification_email(user)

                messages.success(request, "Account created successfully. Please verify your email.")
                return redirect('signin')
            except Exception as e:
                messages.error(request, f"Error creating account: {e}")
                return redirect('register')

    return render(request, 'miniaccounts/register.html')


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from miniaccounts.models import ProfileInfo





def send_verification_email(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_link = f"http://yourdomain.com/verify-email/{uid}/{token}/"
    
    subject = "Verify your email address"
    message = render_to_string('verification_email.html', {'user': user, 'verification_link': verification_link})
    sender_email = "mrdhrubo115@gmail.com"  # Enter your email address here
    recipient_email = user.email
    
    send_mail(subject, message, sender_email, [recipient_email])

def send_verification_email(user):
    token = uuid.uuid4()
    verification_link = f"http://127.0.0.1:8000/register/verify-email/{token}/"
    send_mail(
        'Verify your email address',
        f'Click the link to verify your email: {verification_link}',
        settings.EMAIL_HOST,
        [user.email],
    )
    EmailVerification.objects.create(user=user, token=token)


def verify_email(request, token):
    verification = get_object_or_404(EmailVerification, token=token)
    user = verification.user
    user.is_active = True
    user.save()
    verification.delete()
    messages.success(request, "Email verified successfully. You can now log in.")
    return redirect('register')

def SignIn(request):
    """Handle user sign-in."""
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None:
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('home')  # Redirect to the home page or any other page
            else:
                messages.error(request, "Invalid email or password")
        else:
            messages.error(request, "Invalid email or password")
    users = User.objects.all()
    userinfo = ProfileInfo.objects.all()
   
    context = {
        'users': users,
        'userinfo': userinfo
    }

    
    return render(request, 'miniaccounts/signin.html', context)

from django.contrib.auth.models import User
from .models import ProfileInfo

def ForgotEmail(request):
    if request.method == 'POST':
        remail = request.POST.get('remail')
        
        try:
            # Find the user based on the recovery email address
            user_profile = ProfileInfo.objects.get(remail=remail)
            user = user_profile.user
        except ProfileInfo.DoesNotExist:
            messages.error(request, "No user found with that recovery email address.")
            return redirect('forgot_email')

        # Send email with instructions
        send_reset_email(user)

        messages.success(request, "Instructions to reset your email address have been sent to your email.")
        return redirect('forgot_email')
    
    return render(request, 'miniaccounts/forgot_email.html')

def send_reset_email(user):
    # You can implement the logic to send the email with instructions here
    # For example:
    subject = "Reset Your Email Address"
    message = "This is the email which had been used to create an account. You can sign in using this email."
    sender_email = settings.DEFAULT_FROM_EMAIL
    recipient_email = user.email  # Access remail from the ProfileInfo associated with the user
    
    send_mail(subject, message, sender_email, [recipient_email])



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User


def ForgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        users = User.objects.filter(email=email)

        if not users.exists():
            messages.error(request, "No user found with that email address.")
            return redirect('forgot_password')

        for user in users:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"http://127.0.0.1:8000/register/reset_password/{uid}/{token}/"

            subject = "Reset your password"
            message = render_to_string('miniaccounts/password_reset_email.html', {
                'user': user,
                'reset_link': reset_link
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        messages.success(request, "Instructions to reset your password have been sent to your email.")
        return redirect('signin')

    return render(request, 'miniaccounts/forgot_password.html')


def ResetPassword(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            if password != password2:
                messages.error(request, "Passwords do not match")
                return redirect('reset_password', uidb64=uidb64, token=token)

            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successfully. You can now log in.")
            return redirect('signin')

        return render(request, 'miniaccounts/reset_password.html', {'uidb64': uidb64, 'token': token})
    else:
        messages.error(request, "The reset password link is invalid or has expired.")
        return redirect('forgot_password')



