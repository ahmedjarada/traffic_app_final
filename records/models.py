from django.db import models


class Street(models.Model):
    long = models.FloatField(null=False)
    lat = models.FloatField(null=False)
    title = models.CharField(max_length=128, null=False)


class Record(models.Model):
    prediction = models.PositiveSmallIntegerField(editable=False, null=False, verbose_name='Prediction')
    creation_date = models.DateTimeField(auto_now_add=True)
    street_reference = models.ForeignKey(Street, on_delete=models.CASCADE, related_name='record_st')

# Create your models here.
