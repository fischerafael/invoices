from django.db import models
from django.contrib.auth import get_user_model


CURRENCIES = [
    ("USD", "Dollar"),
    ("GBP", "Pound"),
]


class Client(models.Model):
    name = models.CharField(max_length=256)
    address: models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=256)
    details = models.TextField()
    unit = models.CharField(max_length=128)
    base_rate = models.DecimalField(max_digits=10, decimal_places=2)
    vat = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    number = models.CharField(max_length=30)
    date = models.DateTimeField()
    currency = models.CharField(max_length=10, choices=CURRENCIES)
    payment_currency = models.CharField(max_length=10, choices=CURRENCIES)
    payment_terms = models.CharField(max_length=10)

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    services = models.ManyToManyField(
        Service, through='InvoiceService', blank=True)

    @classmethod
    def find_invoices_by_user_id(cls, user_id: int):
        invoices = cls.objects.filter(user_id=user_id)
        return invoices

    def __calculate_total(self):
        total = 0
        for invoice_service in self.invoiceservice_set.all():
            total += invoice_service.quantity * invoice_service.service.base_rate
        return total

    def __str__(self):
        total = self.__calculate_total()
        return f"{self.number} - {self.date} (Total: {total} {self.currency})"


class InvoiceService(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def calculate_total(self):
        return self.quantity * self.service.base_rate

    def __str__(self):
        return f"{self.service.name} ({self.quantity} {self.service.unit})"
