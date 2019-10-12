from django.shortcuts import render

# Create your views here.
from django.views import View

from charity.models import Donation, Institution


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


class AddDonation(View):
    def get(self, request):
        return render(request, "form.html")


class Login(View):
    def get(self, request):
        return render(request, "login.html")


class Register(View):
    def get(self, request):
        return render(request, "register.html")
