from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

from gifts.forms import RegisterForm, LoginForm, DonationForm, ArchiveForm, ContactForm, SecondDonationForm
from gifts.models import Donation, Institution, Category
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from portfolio_lab import settings
from django.core.mail import send_mail, BadHeaderError
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

    # OBSŁUGA MAILA

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['admin@mail.net'])
            except BadHeaderError as e:
                print(e)
                return HttpResponse('Invalid header found')
            return redirect('confirmation')
    else:
        form = ContactForm()

    context = {
        'form': form,
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
            username = User.objects.get(username=form.cleaned_data['username'])
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth_login(request, user)
                    return HttpResponseRedirect(request.GET.get('next', settings.LOGIN_REDIRECT_URL))
            # return redirect('/addDonation/')
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
    categories = Category.objects.all()
    institutions = Institution.objects.all()

    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/confirmation/')
        else:
            print(form.errors)
    else:
        form = DonationForm()
    return render(request, 'form.html', {'categories': categories, 'institutions': institutions, 'form': form})


def confirmation(request):
    return render(request, 'form-confirmation.html', {})


def profile(request):
    users_donations = Donation.objects.all().filter(user=request.user).order_by('is_taken')

    if request.method == 'POST':
        form = ArchiveForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'profile.html', {'donations': users_donations, 'form': form})
    else:
        form = ArchiveForm()
    return render(request, 'profile.html', {'donations': users_donations, 'form': form})

'''
TO DO LIST:
1. PAGINATORY POPRAWIC I WIDOK WYSWIETLANIA HELP W INDEX.HTML
2. FORMULARZ REGISTER I LOGIN - CLEANED_DATA ETC
'''


def editProfile(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Hasło zostało zmienione')
            return redirect('editProfile')
        else:
            messages.error(request, 'Popraw błędy')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'edit-profile.html', {'form': form})


def donation_two(request):
    categories = Category.objects.all()
    institutions = Institution.objects.all()

    if request.method == 'POST':
        form = SecondDonationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/confirmation/')
    else:
        form = SecondDonationForm()
    return render(request, 'form2.html', {'form': form, 'categories': categories, 'institutions': institutions})


def get_institution_by_categories(request):
    id_cats = request.GET.getlist('cat_ids')
    print(id_cats)
    institutions = Institution.objects.filter(categories__in=id_cats)
    return render(request, 'institution_api.html', {'institutions':institutions})


def get_institution_and_category(request):
    id_cats = request.GET.getlist('cat_ids')
    id_inst = request.GET.get('inst_ids')
    categories = Category.objects.filter(id=id_cats)
    institution = Institution.objects.filter(id=id_inst)
    return render(request, 'cat_inst_api.html', {'categories': categories, 'institution': institution})