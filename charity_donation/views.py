from django.db.models import Count
from django.shortcuts import render

# Create your views here.
from django.views import View
from charity_donation.models import *


class LandingPage(View):
    def get(self, request):
        donations_number = sum(Donation.objects.values_list('quantity', flat=True))
        donated_institutions_number = Donation.objects.values('institution').distinct().count()
        foundations = Institution.objects.filter(type=1)
        organizations = Institution.objects.filter(type=2)
        local_collections = Institution.objects.filter(type=3)
        return render(request, 'charity_donation/index.html',
                      {'donations_number': donations_number,
                       'donated_institutions_number': donated_institutions_number,
                       'foundations': foundations,
                       'organizations': organizations,
                       'local_collections': local_collections})

class AddDonation(View):
    def get(self, request):
        return render(request, 'charity_donation/form.html')

class Login(View):
    def get(self, request):
        return render(request, 'charity_donation/login.html')

class Register(View):
    def get(self, request):
        return render(request, 'charity_donation/register.html')