# from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from gifts.forms import RegisterForm, LoginForm
from gifts.models import Donation, Institution
from django.core.paginator import Paginator

PAGE_SIZE = 5


# Create your views here.
def home(request):
    donation_num = Donation.objects.all().count()
    organisation_num = Institution.objects.all().count()

    # institutions_list = Institution.objects.all()
    fundations_list = Institution.objects.filter(type=1)
    organisations_list = Institution.objects.filter(type=2)
    collections_list = Institution.objects.filter(type=3)

    fundation_paginator = Paginator(fundations_list, PAGE_SIZE)
    organisations_paginator = Paginator(organisations_list, PAGE_SIZE)
    collections_paginator = Paginator(collections_list, PAGE_SIZE)

    fundation_page = request.GET.get('f_page')
    organisations_page = request.GET.get('o_page')
    collections_page = request.GET.get('c_page')


    context = {
        'donation_num': donation_num,
        'organisation_num': organisation_num,
        'pages': {
            'fundation_page': 0,
            'organisations_page': 1,
            'collections_page': 2,


        }


    }
    return render(request, 'index.html', context)


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/addDonation/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']

            form.save()
            return redirect('/login/')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def addDonation(request):
    return render(request, 'form.html', {})


'''
TO DO LIST:
1. PAGINATORY POPRAWIC I WIDOK WYSWIETLANIA HELP W INDEX.HTML
2. FORMULARZ REGISTER I LOGIN - CLEANED_DATA ETC
'''