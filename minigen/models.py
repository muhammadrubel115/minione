from django.db import models
from django.contrib.auth.models import User

import datetime
from django.utils.timezone import get_fixed_timezone


# Create your models here.

from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class MCQPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mcq_posts')
    question = models.CharField(max_length=255)
    reference = models.CharField(max_length=255)
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    
    OPTION_CHOICES = [
        ('option1', 'Option 1'),
        ('option2', 'Option 2'),
        ('option3', 'Option 3'),
        ('option4', 'Option 4'),
    ]
    
    description = models.CharField(max_length=255, choices=OPTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

    def __str__(self):
        return f"{self.question} - by {self.user.username}"

    def count_correct_answers(self):
        return self.responses.filter(is_correct=True).count()

    def count_incorrect_answers(self):
        return self.responses.filter(is_correct=False).count()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'MCQ Post'
        verbose_name_plural = 'MCQ Posts'

class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    mcq_post = models.ForeignKey(MCQPost, on_delete=models.CASCADE, related_name='responses')
    selected_option = models.CharField(max_length=7, choices=MCQPost.OPTION_CHOICES)
    is_correct = models.BooleanField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.is_correct = (self.selected_option == self.mcq_post.answer)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.mcq_post.question} - {self.selected_option}"
    


from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')  # The user receiving the notification
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_notifications')  # The user who triggered the notification
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message}"

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Notification
from miniaccounts.models import ProfileInfo

@receiver(m2m_changed, sender=ProfileInfo.followers.through)
def create_follower_notification(sender, instance, action, reverse, **kwargs):
    if action == 'post_add' and not reverse:
        for pk in kwargs.get('pk_set', []):
            follower = User.objects.get(pk=pk)
            message = f"{follower.username} started following you."
            Notification.objects.create(user=instance.user, follower=follower, message=message)
