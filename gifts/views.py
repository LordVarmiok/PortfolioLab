from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from gifts.forms import RegisterForm, LoginForm
from gifts.models import Donation, Institution
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

PAGE_SIZE = 3


# Create your views here.
def home(request):
    donation_num = Donation.objects.all().count()
    organisation_num = Institution.objects.all().count()

    # institutions_list = Institution.objects.all()
    fundations_list = Institution.objects.filter(type=1)
    organisations_list = Institution.objects.filter(type=2)
    collections_list = Institution.objects.filter(type=3)

    fundation_page = request.GET.get('f_page', default=1)
    organisations_page = request.GET.get('o_page', default=1)
    collections_page = request.GET.get('c_page', default=1)

    fundation_paginator = Paginator(fundations_list, PAGE_SIZE)
    organisations_paginator = Paginator(organisations_list, PAGE_SIZE)
    collections_paginator = Paginator(collections_list, PAGE_SIZE)

    try:
        fundations = fundation_paginator.page(fundation_page)
        organisations = organisations_paginator.page(organisations_page)
        collections = collections_paginator.page(collections_page)
    except PageNotAnInteger:
        fundations = fundation_paginator.page(1)
        organisations = organisations_paginator.page(1)
        collections = collections_paginator.page(1)
    except EmptyPage:
        fundations = fundation_paginator.page(fundation_paginator.num_pages)
        organisations = organisations_paginator.page(organisations_paginator.num_pages)
        collections = collections_paginator.page(collections_paginator.num_pages)


    context = {
        'donation_num': donation_num,
        'organisation_num': organisation_num,

        # PAGINATORS:
        'fundations':fundations,
        'organisations': organisations,
        'collections': collections,

        #     'fundation_page': fundation_page,
        #     'fundation_paginator': fundation_paginator,
        #     'fundations_current_page': 0,
        #
        #
        #     'organisations_page': organisations_page,
        #     'organisations_paginator': organisations_paginator,
        #     'organisations_current_page': 0,
        #
        #
        #     'collections_page': collections_page,
        #     'collections_paginator': collections_paginator,
        #     'collections_current_page': 0,




    }
    return render(request, 'index.html', context)


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            #form.save()
            return redirect('/addDonation/')
        else:
            return redirect('/register/')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
        else:
            print(form.errors)
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