from django.test import TestCase
from .models import User_profile, Order, OrderItem, Address, Product

# Create your tests here.


class StoreTests(TestCase):
    def addItemTest(self):
        """
        This should return True and add an item to the
        OrderItem and also create an Order
        """
        orderitem = OrderItem(user=1, product=2)
        self.assertEqual(orderitem.check(), True)
