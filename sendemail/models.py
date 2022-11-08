from django.db import models

# Create your models here.

class All_users(models.Model):
    username = models.CharField(max_length=50)

    email_address = models.EmailField()
    subs_detail = models.BooleanField(default=False)
