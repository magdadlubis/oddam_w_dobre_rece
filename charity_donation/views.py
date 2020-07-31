from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
from django.views import View
from charity_donation.models import *
from charity_donation.forms import *


class LandingPage(View):
    def get(self, request):
        donations_number = sum(Donation.objects.values_list('quantity', flat=True))
        donated_institutions_number = Donation.objects.values('institution').distinct().count()

        #def paginate(request, objects_list):
            #p = Paginator(objects_list, 5)
            #page_number = request.GET.get('page')
            #objects = p.get_page(page_number)
            #return objects

        foundations_list = Institution.objects.filter(type=1).order_by('name')
        p1 = Paginator(foundations_list, 5)
        page_number = request.GET.get('page')
        foundations = p1.get_page(page_number)

        #foundations = paginate(self.request, foundations_list)

        organizations_list = Institution.objects.filter(type=2).order_by('name')
        p2 = Paginator(organizations_list, 5)
        page_number = request.GET.get('page')
        organizations = p2.get_page(page_number)

        local_collections_list = Institution.objects.filter(type=3).order_by('name')
        p3 = Paginator(local_collections_list, 5)
        page_number = request.GET.get('page')
        local_collections = p3.get_page(page_number)

        return render(request, 'charity_donation/index.html',
                      {'donations_number': donations_number,
                       'donated_institutions_number': donated_institutions_number,
                       'foundations': foundations,
                       'organizations': organizations,
                       'local_collections': local_collections})

class AddDonation(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(request, 'charity_donation/form.html', {
            'categories': categories,
            'institutions': institutions})

    def post(self, request):
        user = request.user
        categories = request.POST.getlist("categories")
        quantity = request.POST.get("bags")
        organization = request.POST.get("organization")
        address = request.POST.get("address")
        city = request.POST.get("city")
        postcode = request.POST.get("postcode")
        phone = request.POST.get("phone")
        pick_up_date = request.POST.get("date")
        pick_up_time = request.POST.get("time")
        pick_up_comment = request.POST.get("more_info")
        institution = Institution.objects.get(id=organization)
        donation = Donation.objects.create(
            quantity=quantity,
            institution=institution,
            address=address,
            phone_number=phone,
            city=city,
            zip_code=postcode,
            pick_up_date=pick_up_date,
            pick_up_time=pick_up_time,
            pick_up_comment=pick_up_comment,
            user=user)
        donation.categories.set(categories)
        return render(request, 'charity_donation/form-confirmation.html')


def get_institution_by_category(request):
    cat_id = request.GET.getlist('cat_id')
    if cat_id is not None:
        categories = Category.objects.filter(pk__in=cat_id)
        print(categories)
        # ZMIENIĆ
        institutions = Institution.objects.filter(categories__in=categories).distinct()
        print(institutions)
    else:
        institutions = Institution.objects.all()
    return render(request, "charity_donation/api_institutions.html", {'institutions': institutions})

class Login(View):
    def get(self, request):
        return render(request, 'charity_donation/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            UserModel.objects.get(username=email)
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('landing-page')
            else:
                msg = 'Niepoprawne hasło'
                return render(request, 'charity_donation/login.html', {'msg': msg})
        except ObjectDoesNotExist:
            return redirect('register')


class Register(View):
    def get(self, request):
        return render(request, 'charity_donation/register.html')

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if not UserModel.objects.filter(email=email):
            if password == password2:
                UserModel.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name=name,
                    last_name=surname)
                return redirect('login')
            else:
                msg = 'Hasła się różnią'
                return render(request, 'charity_donation/register.html', {'msg_passwords': msg})
        else:
            msg = 'Nazwa użytkownika (e-mail) jest już w użyciu!'
            return render(request, 'charity_donation/register.html', {'msg_username': msg})


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('landing-page')


class Profile(LoginRequiredMixin, View):
    def get(self, request):
        # ZROBIĆ SORTOWANIE!!!
        completed_donations = Donation.objects.filter(user=request.user).\
            filter(is_taken=1).\
            order_by('picked_up_date', 'date_added')
        prepared_donations = Donation.objects.filter(user=request.user).\
            filter(is_taken=0).\
            order_by('date_added')
        return render(request, 'charity_donation/profile.html', {'completed_donations': completed_donations,
                                                                 'prepared_donations': prepared_donations})


class EditDonation(View):
    def get(self, request, donation_id):
        donation = Donation.objects.get(pk=donation_id)
        form = EditDonationForm(instance=donation)
        return render(request, 'charity_donation/edit_donation.html', {'form': form})

    def post(self, request, donation_id):
        donation = Donation.objects.get(pk=donation_id)
        form = EditDonationForm(request.POST)
        if form.is_valid():
            picked_up_date = form.cleaned_data['picked_up_date']
            donation.picked_up_date = picked_up_date
            donation.is_taken = 1
            donation.save()
            return redirect('profile')
        return render(request, 'charity_donation/edit_donation.html', {'form': form})