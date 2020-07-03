from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

INSTITUTION_TYPE = (
    (1, 'fundacja'),
    (2, 'organizacja pozarządowa'),
    (3, 'zbiórka lokalna')
)

UserModel = get_user_model()

class Category(models.Model):
    name = models.CharField(verbose_name='Nazwa kategorii', max_length=128)


class Institution(models.Model):
    name = models.CharField(verbose_name='Nazwa instytucji', max_length=128)
    description = models.TextField(verbose_name='Opis')
    type = models.IntegerField(verbose_name='Rodzaj instytucji', choices=INSTITUTION_TYPE, default=1)
    categories = models.ManyToManyField(Category)


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