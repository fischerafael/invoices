from typing import List

from django.db.models import Sum
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from invoices import models
from invoices.use_cases import InvoicesUseCases
from users.models import CustomUser


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email']


class ServiceSerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField()

    class Meta:
        model = models.Service
        fields = '__all__'

    def get_quantity(self, service):
        invoice_services = models.InvoiceService.objects.filter(
            service=service)
        print(invoice_services)
        return 0


class InvoicesSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    user = UserSerializer()
    services = ServiceSerializer(many=True, read_only=True)

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
