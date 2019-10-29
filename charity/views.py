from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
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

        return render(request, 'index.html', ctx)


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
            return render(request, 'form.html', ctx)
        else:
            return redirect('login')

    def post(self, request):
        categories = request.POST.getlist('categories')
        bags = request.POST.get('bags')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        pick_up_date = request.POST.get('data')
        time = request.POST.get('time')
        comment = request.POST.get('more_info')
        institution = request.POST.get('organization')
        user = request.user

        new_donation = Donation.objects.create(quantity=bags,
                                               address=address,
                                               phone_number=phone,
                                               city=city,
                                               zip_code=postcode,
                                               pick_up_date=pick_up_date,
                                               pick_up_time=time,
                                               pick_up_comment=comment,
                                               institution_id=institution,
                                               user_id=user.id)
        new_donation.categories.set(categories)

        return redirect('thank_you')


class DonationConfirmation(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('landing_page')
        else:
            return redirect('register')


class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            if not User.objects.get(email=email):
                User.objects.create_user(first_name=name,
                                         last_name=surname,
                                         email=email,
                                         password=password,
                                         username=email)
            else:
                messages.error(request, 'User with this email already exists.')
                return redirect('register')

        return redirect('login')


class Profile(View):
    def get(self, request):
        ctx = {}
        donations = Donation.objects.filter(user_id=request.user.id).order_by('is_taken', '-pick_up_date')

        ctx['user'] = request.user
        ctx['donations'] = donations

        return render(request, 'profile.html', ctx)

    def post(self, request):
        if request.POST.get('archive'):
            donation = Donation.objects.get(id=request.POST.get('archive'))
            donation.is_taken = True
            donation.save()
            return redirect('profile')


class EditProfile(View):
    def get(self, request):
        ctx = {}
        ctx['user'] = request.user

        return render(request, 'profile-edit.html', ctx)

    def post(self, request):
        user = User.objects.get(id=request.user.id)

        if user.check_password(request.POST['old-password']):
            user.first_name = request.POST.get('name')
            user.last_name = request.POST.get('surname')
            user.email = request.POST.get('email')
            user.username = request.POST.get('email')

            if request.POST.get('password') and request.POST.get('password') == request.POST.get('password2'):
                user.set_password(request.POST.get('password'))
                update_session_auth_hash(request, user)
        else:
            messages.error(request, 'Hasło nieprawidłowe. Podaj hasło, żeby zapisać zmiany.')
            return redirect('edit')

        user.save()
        messages.success(request, 'Zmiany zostały zapisane.')
        return redirect('profile')
