from typing import List

from invoices.models import Invoice


class InvoicesUseCases():

    invoice_model = Invoice()

    def list_invoices_by_user(self, user_id: int) -> List[Invoice]:
        invoices = self.invoice_model.find_invoices_by_user_id(user_id=user_id)
        return invoices
