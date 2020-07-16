from django.contrib.auth.models import User
from django.db import models

TYPES = (
    ('fundacja', 'fundacja'),
    ('organizacja pozarzadowa', 'organizacja pozarzadowa'),
    ('zbiorka lokalna', 'zbiorka lokalna')
)


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128)


class Institution(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    type = models.CharField(choices=TYPES, default='fundacja', max_length=24)
    categories = models.ManyToManyField(Category)


class Donation(models.Model):
    quantity = models.IntegerField()# ilosc workow
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=128)# adres dawcy
    phone_number = models.CharField(max_length=12) # nr tel dawcy
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, default='Null', on_delete=models.CASCADE)