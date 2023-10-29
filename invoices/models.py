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


class Invoice(models.Model):
    number = models.CharField(max_length=30)
    date = models.DateTimeField()
    currency = models.CharField(max_length=10, choices=CURRENCIES)
    payment_currency = models.CharField(max_length=10, choices=CURRENCIES)
    payment_terms = models.CharField(max_length=10)

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return super().__str__()


class Service(models.Model):
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=256)
    details = models.TextField()
    unit = models.CharField(max_length=128)
    quantity = models.PositiveIntegerField(default=1)
    base_rate = models.DecimalField(max_digits=10, decimal_places=2)
    vat = models.DecimalField(max_digits=10, decimal_places=2)
