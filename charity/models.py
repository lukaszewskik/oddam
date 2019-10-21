from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
TYPES = ((1, 'Fundacja'),
         (2, 'Organizacja pozarządowa'),
         (3, 'Zbiórka lokalna'))


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Institution(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    type = models.IntegerField(choices=TYPES, default=1)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=64)
    phone_regex = RegexValidator(regex=r'^\+?\d{9,15}$',
                                 message="Numer telefonu musi być w formacie: '+999999999'. Max. 15 cyfr")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    city = models.CharField(max_length=64)
    zip_code_regex = RegexValidator(regex=r'^\d{2}-\d{3}$',
                                    message="Kod pocztowy musi być w formacie: '00-000'.")
    zip_code = models.CharField(validators=[zip_code_regex], max_length=6, blank=True)
    pick_up_date = models.DateField(auto_now_add=False)
    pick_up_time = models.TimeField(null=True)
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
