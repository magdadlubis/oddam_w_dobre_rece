from django.contrib.auth import get_user_model
from django.db import models
from datetime import date

# Create your models here.

INSTITUTION_TYPE = (
    (1, 'fundacja'),
    (2, 'organizacja pozarządowa'),
    (3, 'zbiórka lokalna')
)

STATUS = (
    (0, 'nieodebrane'),
    (1, 'odebrane'),
)

UserModel = get_user_model()

class Category(models.Model):
    name = models.CharField(verbose_name='Nazwa kategorii', max_length=128)

    def __str__(self):
        return '{}'.format(self.name)


class Institution(models.Model):
    name = models.CharField(verbose_name='Nazwa instytucji', max_length=128)
    description = models.TextField(verbose_name='Opis')
    type = models.IntegerField(verbose_name='Rodzaj organizacji', choices=INSTITUTION_TYPE, default=1)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return '{}'.format(self.name)


class Donation(models.Model):
    quantity = models.PositiveIntegerField(verbose_name='Liczba worków')
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(verbose_name='Ulica i numer domu', max_length=128)
    phone_number = models.PositiveIntegerField(verbose_name='Numer telefonu')
    city = models.CharField(verbose_name='Miasto', max_length=64)
    zip_code = models.CharField(verbose_name='Kod pocztowy', max_length=6)
    pick_up_date = models.DateField(verbose_name='Dzień odbioru')
    pick_up_time = models.TimeField(verbose_name='Godzina odbioru')
    pick_up_comment = models.TextField(verbose_name='Uwagi do odbioru', blank=True)
    user = models.ForeignKey(UserModel, null=True, default=None, on_delete=models.CASCADE)
    is_taken = models.IntegerField(choices=STATUS, default=0)
    picked_up_date = models.DateTimeField(verbose_name='Data odbioru', null=True)
    date_added = models.DateTimeField(auto_now_add=True)