import calendar

from django.db import models
from datetime import datetime


# Create your models here.
class Area(models.Model):
    class Meta:
        ordering  = ('name', 'created_at')
    name= models.CharField(max_length=200)
    status = models.BooleanField()
    created_at = models.DateTimeField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = datetime.now()
        res = super().save(args, kwargs)
        return res


class PackageType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Package(models.Model):
    class Meta:
        pass
        #verbose_name_plural = 'Sami'
        
    name= models.CharField(max_length=200)
    status = models.BooleanField()
    package_type = models.ForeignKey(PackageType, on_delete=models.CASCADE, related_name='packages', null=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = datetime.now()
        res = super().save(args, kwargs)
        return res


class Client(models.Model):
    name= models.CharField(max_length=200)
    status = models.BooleanField()

    price = models.IntegerField()
    connection_charges= models.IntegerField()
    connection_date = models.DateField()
    pending = models.IntegerField(default=0)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='clients')
    last_payment_date = models.DateField(blank=True, null=True)
    next_payment_date = models.DateField()

    father_name= models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    cnic = models.CharField(max_length=200, null=True, blank=True)
    address= models.CharField(max_length=1024, null=True, blank=True)

    created_at = models.DateTimeField()

    class Meta:
        ordering = ('next_payment_date',)
        pass
        # verbose_name_plural = 'Sami'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = datetime.now()
            self.pending = self.price + self.connection_charges
        res = super().save(args, kwargs)
        return res


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)


def add_one_month_to_date(given_date):
    return add_months(given_date, 1)


class Payment(models.Model):
    class Meta:
        pass
        #verbose_name_plural = 'Sami'

    client= models.ForeignKey(Client, related_name='payment', on_delete=models.CASCADE)
    amount = models.IntegerField()
    payment_date = models.DateField()
    created_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = datetime.now()
            self.client.pending = self.client.pending - self.amount            
            self.client.save()
        res = super().save(args, kwargs)
        return res
