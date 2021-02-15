from django.db import models
from datetime import datetime
from .import methods
from django.contrib.auth.models import User


class DefaultClass(models.Model):
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_query_name='%(app_label)s_%(class)s_created_by',
        related_name='%(app_label)s_%(class)s_created_by'
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='%(app_label)s_%(class)s_updated_by',
        related_query_name='%(app_label)s_%(class)s_updated_by'
    )

    class Meta:
        abstract = True


class AreaManager(models.Manager):
    def get_queryset(self):
        res = super().get_queryset().filter(status=True)
        return res


class AreaManagerAll(models.Manager):
    def get_queryset(self):
        res = super().get_queryset()
        return res


class Area(DefaultClass):
    class Meta:
        ordering = ('-status', 'name', 'created_at')

    objects = AreaManager()
    full = AreaManagerAll()
    name = models.CharField(max_length=200)
    status = models.BooleanField()

    def __str__(self):
        return self.name


class PackageType(DefaultClass):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Package(DefaultClass):
    class Meta:
        pass

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


class Client(DefaultClass):
    name= models.CharField(max_length=200)
    area = models.ForeignKey(Area, related_name='clients', on_delete=models.CASCADE)

    father_name= models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    cnic = models.CharField(max_length=200, null=True, blank=True)
    address= models.CharField(max_length=1024, null=True, blank=True)
    # balance is here...

    balance = models.IntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField()

    class Meta:
        ordering = ('area', 'name')
        pass
        # verbose_name_plural = 'Sami'

    def __str__(self):
        return self.name

    def is_defaulter(self):
        pass


class Subscription(DefaultClass):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='subscriptions')
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    connection_charges = models.IntegerField(default=0)
    connection_date = models.DateField()
    expiry_date = models.DateField(null=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.client.name + '-' + self.package.name

    def save(self, *args, **kwargs):
        if not self.expiry_date:
            self.active = False
        res = super().save(args, kwargs)
        return res


class Payment(DefaultClass):
    class Meta:
        pass

    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    amount = models.IntegerField()
    payment_date = models.DateField()
    price_charged = models.IntegerField(default=0)
    created_at = models.DateTimeField()
    renewal_start_date = models.DateField()
    renewal_end_date = models.DateField()

    def __str__(self):
        return '{}-{}'.format(self.subscription.__str__(), self.amount)

    def save(self, *args, **kwargs):
        renewal_start_date = self.renewal_start_date or self.payment_date
        price_charged = self.subscription.price

        # in case of first subscription or subscription after service terminated
        customer_balance = self.subscription.client.balance or 0
        if (not self.subscription.active) or (len(self.subscription.payments) <= 1):
            price_charged += self.subscription.connection_charges

        if self.subscription.active:
            last_obj = Payment.objects.filter(subscription_id=self.subscription.id).order_by('renewal_end_date').last()
            if len(last_obj):
                if last_obj.renewal_end_date > self.renewal_start_date:
                    diff_days = get_days_difference(last_obj.renewal_start_date, last_obj.renewal_end_date)
                    renewal_start_date = add_days(last_obj.renewal_start_date, diff_days)

        balance = self.subscription.client.balance or 0
        amount = self.amount

        self.price_charged = price_charged
        if self.pk:
            last_payment = Payment.objects.filter(id=self.pk)[0]
            amount -= last_payment.amount
            price_charged -= last_payment.price_charged

        self.subscription.client.balance = customer_balance + amount - price_charged
        self.subscription.client.save()
        self.renewal_start_date = renewal_start_date
        renewal_end_date = add_one_month_to_date(renewal_start_date)
        self.renewal_end_date = renewal_end_date
        self.subscription.expiry_date = renewal_end_date

        res = super().save(args, kwargs)
        self.subscription.save()
        return res


def add_months(source_date, months):
    res = methods.add_interval('months', months, source_date)
    return res


def add_one_month_to_date(given_date):
    given_date = methods.add_interval('days', -1, given_date)
    return add_months(given_date, 1)


def get_days_difference(start_date, end_date):
    seconds = methods.dt_span_seconds(start_date, end_date)
    days = seconds / 60 / 60 / 24
    days = round(days)
    return days


def add_days(dt1, days):
    res = methods.add_interval('days', days, dt1)
    return res