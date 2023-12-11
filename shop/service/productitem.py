# create a new instance of ProductItem object from product 

from shop.models import ProductItem


def addproductitem(product):
    productitem = ProductItem()
    productitem.product = product
    productitem.quantity = product.quantity
    productitem.color = product.color
    productitem.size = product.size
    productitem.save()
    return productitem