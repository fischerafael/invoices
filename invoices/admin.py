from django import forms
from django.contrib import admin

from invoices.models import Client, Invoice, InvoiceService, Service

# Register your models here.


class ServiceInline(admin.TabularInline):
    model = InvoiceService
    extra = 1


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'client')
    inlines = [ServiceInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Service, ServiceAdmin)
