from django.db import models

# Create your models here.

INSTITUTION_TYPE = (
    (1, 'fundacja'),
    (2, 'organizacja pozarządowa'),
    (3, 'zbiórka lokalna')
)

class Category(models.Model):
    name = models.CharField(verbose_name='Nazwa kategorii', max_length=128)


class Institution(models.Model):
    name = models.CharField(verbose_name='Nazwa instytucji', max_length=128)
    description = models.TextField(verbose_name='Opis')
    type = models.IntegerField(verbose_name='Rodzaj instytucji', choices=INSTITUTION_TYPE, default=1)
    categories = models.ManyToManyField(Category)