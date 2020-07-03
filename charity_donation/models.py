from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(verbose_name='Nazwa kategorii', max_length=128)