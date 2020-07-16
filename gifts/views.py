from django.shortcuts import render
from gifts.models import Donation, Institution


# Create your views here.
def home(request):
    donation_num = Donation.objects.all().count()
    organisation_num = Institution.objects.all().count()

    context = {'donation_num': donation_num, 'organisation_num': organisation_num}
    return render(request, 'index.html', context)


def login(request):
    return render(request, 'login.html', {})


def register(request):
    return render(request, 'register.html', {})


def addDonation(request):
    return render(request, 'form.html', {})