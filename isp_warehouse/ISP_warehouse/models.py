from django.db import models
from datetime import datetime


class Supplier(models.Model):
    name = models.TextField()
    address = models.TextField(null=True, blank=True, default="")
    phone = models.TextField(null=True, blank=True, default="")
    director = models.TextField(null=True, blank=True, default="")
    email = models.EmailField(null=True, blank=True, default="")
    web = models.TextField(null=True, blank=True, default="")
    notes = models.TextField(null=True, blank=True, default="")


class Category(models.Model):
    name = models.TextField(unique=True)


class Type(models.Model):
    name = models.TextField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class LocType(models.Model):
    name = models.TextField(unique=True)


class Location(models.Model):
    name = models.TextField()
    loc_type = models.ForeignKey(LocType, on_delete=models.CASCADE)


class Inventory(models.Model):
    inv_type = models.ForeignKey(Type, on_delete=models.CASCADE)
    document = models.FileField(null=True, blank=True, default=None, upload_to='documents/%Y/%m/%d')
    serial_num = models.TextField(unique=True)
    image = models.ImageField(null=True, blank=True, default="pictures/noimg.png", upload_to='pictures/%Y/%m/%d')
    cost = models.IntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True, default="")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)


class Operation(models.Model):
    date = models.DateTimeField(default=datetime.now())
    from_place = models.ForeignKey(Location, null=False, related_name='from_place', on_delete=models.CASCADE)
    destination = models.ForeignKey(Location, null=False, related_name='destination', on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    author = models.ForeignKey(Location, null=False, related_name='author', on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True, default="")
