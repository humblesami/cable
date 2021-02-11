from django.db import models
from datetime import datetime
from .import methods


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
    rate = models.IntegerField()
    valid_for_months = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = datetime.now()
        res = super().save(args, kwargs)
        return res


class Client(models.Model):
    name= models.CharField(max_length=200)
    area = models.ForeignKey(Area, related_name='clients', on_delete=models.CASCADE)

    father_name= models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    cnic = models.CharField(max_length=200, null=True, blank=True)
    address= models.CharField(max_length=1024, null=True, blank=True)

    created_at = models.DateTimeField()

    class Meta:
        ordering = ('area', 'name')
        pass
        # verbose_name_plural = 'Sami'

    def __str__(self):
        return self.name

    def is_defaulter(self):
        pass

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = datetime.now()
            self.pending = self.price + self.connection_charges
        res = super().save(args, kwargs)
        return res


class ClientPackage(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    price = models.IntegerField()
    connection_charges = models.IntegerField()
    connection_date = models.DateField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.client.name + '-' + self.package.name


class Payment(models.Model):
    class Meta:
        pass
        #verbose_name_plural = 'Sami'

    client_package = models.ForeignKey(ClientPackage, on_delete=models.CASCADE)
    amount = models.IntegerField()
    payment_date = models.DateField()
    created_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        creating = False
        if not self.pk:
            creating = True
            self.created_at = datetime.now()
        res = super().save(args, kwargs)

        if creating:
            self.client_package.client.balance + self.amount
            self.client_package.client.save()

            new_subscription = Subscription(
                client_pakage_id=self.client_package.id,
                start_date=self.payment_date,
                payment_id=self.id
            )
            new_subscription.save()

        return res


class Subscription(models.Model):
    client_package = models.ForeignKey(ClientPackage, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        price = self.client_package.price
        # in case of first subscription or subscription after service terminated
        if not self.client_package.active:
            price += self.client_package.connection_charges
        if self.client_package.active:
            obj = Subscription.objects.filter(client_package_id=self.client_package.id).order_by('end_date')
            if len(obj):
                last_obj = obj[len(obj) - 1]
                if last_obj.end_date > self.start_date:
                    diff_days = get_days_difference(last_obj.start_date, last_obj.end_date)
                    self.start_date = add_days(last_obj.start_date, diff_days)

        months = price % self.client.balance
        end_date = add_months(self.start_date, months)
        self.end_date=end_date
        res = super().save()
        return res


def add_months(source_date, months):
    res = methods.add_interval('months', months, source_date)
    return res


def add_one_month_to_date(given_date):
    return add_months(given_date, 1)


def get_days_difference(start_date, end_date):
    seconds = methods.dt_span_seconds(start_date, end_date)
    days = seconds / 60 / 60 / 24
    days = round(days)
    return days


def add_days(dt1, days):
    res = methods.add_interval('days', days, dt1)
    return res