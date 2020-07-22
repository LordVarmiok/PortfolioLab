from django.contrib import admin
from django.contrib.auth.models import User

from .models import Category, Institution, Donation
# Register your models here.
admin.site.register(Category)
admin.site.register(Institution)
admin.site.register(Donation)
# admin.site.register(User)