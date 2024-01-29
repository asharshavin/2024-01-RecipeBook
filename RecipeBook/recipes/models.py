from django.db import models


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=150)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Dish(models.Model):
    title = models.CharField(max_length=150)
    product = models.ManyToManyField(Product, through='Composition')

    def __str__(self):
        return self.title


class Composition(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    volume = models.IntegerField(default=0, null=True)
