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


# class AreaManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(active=True)


class Area(DefaultClass):
    class Meta:
        ordering  = ('name', 'created_at')

    #objects = AreaManager()
    name= models.CharField(max_length=200)
    status = models.BooleanField()
    # created_at = models.DateTimeField()

    def __str__(self):
        return self.name


class PackageType(DefaultClass):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Package(DefaultClass):
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


class ClientPackage(DefaultClass):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    connection_charges = models.IntegerField(default=0)
    connection_date = models.DateField()
    active = models.BooleanField(default=False)


    def __str__(self):
        return self.client.name + '-' + self.package.name

    def save(self, *args, **kwargs):
        res = super().save(args, kwargs)
        self.client.balance = self.price + self.connection_charges
        self.client.save()
        return res


class Payment(DefaultClass):
    class Meta:
        pass
        #verbose_name_plural = 'Sami'

    client_package = models.ForeignKey(ClientPackage, on_delete=models.CASCADE)
    amount = models.IntegerField()
    payment_date = models.DateField()
    created_at = models.DateTimeField()
    is_renew = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return '{}-{}-{}'.format(self.client_package.client.name, self.amount, self.payment_date)



    def save(self, *args, **kwargs):
        creating = False
        if not self.pk:
            creating = True
            self.created_at = datetime.now()
        res = super().save(args, kwargs)

        if creating:
            # price = self.client_package.price if self.client_package.price else 0
            # balance = self.client_package.client.balance if self.client_package.client.balance else 0
            # total_payable = price + balance
            # remaining_payables = total_payable - self.amount
            # if remaining_payables < 0:
            #     # in case client pay extra amount in advance
            #     pass
            # else:
            #     self.client_package.client.balance = remaining_payables
            #     self.client_package.client.save()

            new_subscription = Subscription(
                client_package_id=self.client_package.id,
                start_date=self.payment_date,
                payment_id=self.id
            )
            new_subscription.save()

        return res


class Subscription(DefaultClass):
    client_package = models.ForeignKey(ClientPackage, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)

    def __str__(self):
        return 'Subscription-{}-{}-From: {}-To: {}'.format(self.client_package.client.name, self.payment.amount, self.start_date, self.end_date)


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

        balance = self.client_package.client.balance
        balance = balance if balance else 0

        if balance > price:
            # in case of advance payment

            # months = price % self.client_package.client.balance
            # end_date = add_months(self.start_date, months)
            # self.end_date=end_date
            pass
        else:
            amount = self.payment.amount
            amount = amount if amount else 0
            payable = 0
            if self.payment.is_renew:
                package_price = self.client_package.price
                package_price = package_price if package_price else 0
                payable = balance + package_price - amount
            else:
                payable = balance - amount
            self.client_package.client.balance = payable
            self.client_package.client.save()
            self.end_date = add_one_month_to_date(self.start_date)
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