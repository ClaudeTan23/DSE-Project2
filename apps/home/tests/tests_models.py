from django.test import TestCase
from apps.home.models import Product
# py manage.py test --pattern="tests_*.py"
class ProductModelTest(TestCase):


    def test_create_product(self):
        
        product = Product.objects.create(
            name="Test Product",
            sku="SKU001",
            category="Electronics",
            price=10.50,
            stock=5
        )
        
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.stock, 5)
        print(f"{self.__class__.__name__} Passed")