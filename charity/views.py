from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from charity.models import Donation, Institution, Category


class LandingPage(View):
    def get(self, request):
        ctx = {}
        donations = Donation.objects.all()
        foundations = Institution.objects.filter(type=1)
        organizations = Institution.objects.filter(type=2)
        local = Institution.objects.filter(type=3)

        institutions_qt = Institution.objects.all().count()
        donated_qt = 0
        for donation in donations:
            donated_qt += donation.quantity

        ctx['donated_qt'] = donated_qt
        ctx['institutions_qt'] = institutions_qt
        ctx['foundations'] = foundations
        ctx['organizations'] = organizations
        ctx['local'] = local

        return render(request, "index.html", ctx)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('landing_page')


class AddDonation(View):
    def get(self, request):
        if request.user.is_authenticated:
            ctx = {}
            categories = Category.objects.all()
            institutions = Institution.objects.all()
            ctx['categories'] = categories
            ctx['institutions'] = institutions
            return render(request, "form.html", ctx)
        else:
            return redirect('login')

    def post(self, request):
        bags = request.POST['bags']
        address = request.POST['address']
        city = request.POST['city']
        postcode = request.POST['postcode']
        phone = request.POST['phone']
        pick_up_date = request.POST['data']
        time = request.POST['time']
        comment = request.POST['more_info']
        institution = request.POST['organization']
        return redirect('add_donation')


class Login(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("landing_page")
        else:
            return redirect("register")


class Register(View):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        print(name, surname)
        if password == password2:
            # TODO: check if user exists
            User.objects.create_user(first_name=name,
                                     last_name=surname,
                                     email=email,
                                     password=password,
                                     username=email)

        return redirect("login")
