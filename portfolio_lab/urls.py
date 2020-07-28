"""portfolio_lab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from gifts import views
from django.contrib.auth.views import LogoutView

from portfolio_lab import settings

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.home, name='landingPage'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('addDonation/', views.addDonation, name='addDonation'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    # path('', include('django.contrib.auth.urls'))
    path('profile/', views.profile, name='profile'),
    path('editProfile/', views.editProfile, name='editProfile'),
    path('confirmation/', views.confirmation, name='confirmation')
]
