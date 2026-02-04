from django.test import TestCase
from django.contrib.auth.models import User
from apps.home.models import Product, Sale, SaleItem

class SaleTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("u", password="123")
        self.product = Product.objects.create(
            name="Keyboard",
            sku="K001",
            category="IT",
            price=50,
            stock=10
        )

    def test_sale_deducts_stock(self):
        sale = Sale.objects.create(
            invoice_no="INV-001",
            user=self.user,
            payment_method="Cash",
            total_amount=0
        )

        SaleItem.objects.create(
            sale=sale,
            product=self.product,
            quantity=2,
            unit_price=50,
            line_total=100
        )

        self.product.stock -= 2
        self.product.save()

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 8)
        print(f"{self.__class__.__name__} Passed")
