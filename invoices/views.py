from typing import List

from django.db.models import Sum
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from invoices import models
from invoices.use_cases import InvoicesUseCases
from users.models import CustomUser


class InvoicesSerializerClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        exclude = ['id']


class InvoicesSerializerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name']


class InvoicesSerializerServiceSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()
    vat = serializers.SerializerMethodField()

    def get_rate(self, obj):
        return float(obj.base_rate)

    def get_vat(self, obj):
        return float(obj.vat)

    class Meta:
        model = models.Service
        fields = ['name', 'details', 'unit', 'rate', 'vat']


class InvoicesSerializerInvoiceServiceSerializer(serializers.ModelSerializer):
    service = InvoicesSerializerServiceSerializer()

    class Meta:
        model = models.InvoiceService
        fields = ['quantity', 'service']


class InvoicesSerializer(serializers.ModelSerializer):
    client = InvoicesSerializerClientSerializer()
    user = InvoicesSerializerUserSerializer()
    services = InvoicesSerializerInvoiceServiceSerializer(
        many=True, source='invoiceservice_set')

    class Meta:
        model = models.Invoice
        fields = '__all__'


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def list_invoices(request):

    user_id = 1
    use_case = InvoicesUseCases()

    invoices = use_case.list_invoices_by_user(user_id=user_id)

    serializer = InvoicesSerializer(invoices, many=True)

    return Response(serializer.data)
