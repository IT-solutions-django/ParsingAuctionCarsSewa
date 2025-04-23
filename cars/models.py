from django.db import models


class AuctionCars(models.Model):
    api_id = models.CharField(max_length=500, verbose_name='ID авто')
    brand = models.CharField(max_length=500, null=True, blank=True, verbose_name='Марка')
    model = models.CharField(max_length=500, null=True, blank=True, verbose_name='Модель')
    grade = models.CharField(max_length=500, null=True, blank=True, verbose_name='Комплектация')
    year = models.IntegerField(null=True, blank=True, verbose_name='Год')
    fuel = models.CharField(max_length=500, null=True, blank=True, verbose_name='Тип топлива')
    transmission = models.CharField(max_length=500, null=True, blank=True, verbose_name='Тип КПП')
    color = models.CharField(max_length=500, null=True, blank=True, verbose_name='Цвет')
    mileage = models.IntegerField(null=True, blank=True, verbose_name='Пробег')
    photos = models.TextField(null=True, blank=True, verbose_name='Фотографии')

    def __str__(self):
        return f'{self.brand} {self.model} {self.year}'



