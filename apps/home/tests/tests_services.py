from django.test import TestCase
from apps.home.services.invoice_service import generate_invoice_no
from apps.home.models import Sale

class InvoiceServiceTest(TestCase):

    def test_invoice_increment(self):
        inv1 = generate_invoice_no()
        Sale.objects.create(
            invoice_no=inv1,
            total_amount=10,
            payment_method="Cash"
        )

        inv2 = generate_invoice_no()
        self.assertNotEqual(inv1, inv2)
        print(f"{self.__class__.__name__} Passed")
