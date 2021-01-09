from django.db import models
from user.models import User


class History(models.Model):
    lat = models.FloatField(null=False)
    long = models.FloatField(null=False)
    title = models.CharField(default='Location history', max_length=128)
    creation_date = models.DateTimeField(editable=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='User_history', null=False, editable=False)

# Create your models here.
