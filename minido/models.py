
# Create your imports here.
from django.db import models


# Custom User Models

class FAQ(models.Model):
    id=models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    faqbody = models.CharField(max_length=1000)
    date = models.DateField(null=True)

    def __str__(self):
        return self.fullname
    
