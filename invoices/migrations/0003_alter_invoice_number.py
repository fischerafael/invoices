# Generated by Django 4.2.6 on 2023-10-31 21:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0002_alter_invoice_date_alter_invoice_payment_terms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='number',
            field=models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(8)]),
        ),
    ]