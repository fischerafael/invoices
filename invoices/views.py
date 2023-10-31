from typing import List

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from invoices.models import Invoice
from invoices.use_cases import InvoicesUseCases
from users.models import CustomUser


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def list_invoices(request):

    user_id = 1
    use_case = InvoicesUseCases()

    invoices = use_case.list_invoices_by_user(user_id=user_id)
    print('************* ', invoices)

    return Response('Hey')
