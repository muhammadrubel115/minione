from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User
import uuid

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import uuid

# Define your models here.

class ProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    acc_name=models.CharField(max_length=70, blank=True, null=True)
    bio = models.CharField(max_length=70, blank=True, null=True)
    acc_type = models.CharField(max_length=70, blank=True, null=True)
    country = models.CharField(max_length=70, blank=True, null=True)
    gender = models.CharField(
        max_length=70,
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other')
        ],
        blank=True,
        null=True
    )
    dob = models.DateField(blank=True, null=True)
    email = models.EmailField(max_length=70, blank=True, null=True)
    remail = models.EmailField(max_length=70, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    acc_creation_time = models.DateTimeField(auto_now_add=True)



    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    following = models.ManyToManyField(User, related_name='following', blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Profile Info"
        verbose_name_plural = "Profile Infos"
        ordering = ['-acc_creation_time']


    def clean(self):
        from django.core.exceptions import ValidationError
        if self.phone and not self.phone.isdigit():
            raise ValidationError('Phone number must contain only digits.')
        # Add more validations as required
# Optional: Consider adding validation for phone numbers and other fields if necessary.



class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"EmailVerification for {self.user.username} with token {self.token}"

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=128)  # Adjust length as needed for the token
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Token for {self.user.username} created on {self.created_at}"

    class Meta:
        verbose_name = "Password Reset Token"
        verbose_name_plural = "Password Reset Tokens"
        ordering = ['-created_at']

