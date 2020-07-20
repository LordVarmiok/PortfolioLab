from django.shortcuts import render
from gifts.models import Donation, Institution
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    donation_num = Donation.objects.all().count()
    organisation_num = Institution.objects.all().count()

    institutions_list = Institution.objects.all()
    paginator = Paginator(institutions_list, 5)
    page = request.GET.get('page')
    institutions = paginator.get_page(page)

    context = {
        'donation_num': donation_num,
        'organisation_num': organisation_num,
        'institutions': institutions,
        'paginator':paginator,
    }
    return render(request, 'index.html', context)


def login(request):
    return render(request, 'login.html', {})


def register(request):
    return render(request, 'register.html', {})


def addDonation(request):
    return render(request, 'form.html', {})