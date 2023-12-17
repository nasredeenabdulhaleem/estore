"""
  item = {
        "product_title": title,
        "product_slug" : slug,
        "product_desc" : desc,
        "product_image": image,
        "product_price": price,
        "product_discount": discount,
        "product_category": category,
        "product_variant": {
            "color": {
                "blue": {
                          "size" :["xs", "s", "l", "xl", "xxl"],
                          "amount_in_stock": 5,
                        },
                "green": {
                          "size" :["xs", "s", "l", "xl", "xxl"],
                          "amount_in_stock": 5,
                        },
                "grey": {
                          "size" :["xs", "s", "l", "xl", "xxl"],
                          "amount_in_stock": 5,
                        },
                "brown": {
                          "size" :["xs", "s", "l", "xl", "xxl"],
                          "amount_in_stock": 5,
                        }
            }
        },
    }
"""

from django.core import serializers
from shop.models import Product, ProductVaraiant
from django.forms.models import model_to_dict
from PIL import Image
from django.forms.models import model_to_dict
from itertools import chain

# from rest_framework import serializers
from .serializers import product_variant_serializer, size_serializer
import json

# {
#     'product_title': 'Wrist watch',
#     'product_slug': '19a9515d-c8c8-11ed-9b60-8b569fb40be2',
#     'product_desc': 'blablu blu blu bulaba',
#     'product_image': '/media/product-home-image/pexels-chloe-1043473_kwQltYP.jpg',
#     'product_price': 800.0,
#     'product_discount': None,
#     'product_category': 'Accessories',
#     'product_variant': {
#         'RED':
#             '[{"model": "shop.size", "pk": 6, "fields": {"size": "m"}}, {"model": "shop.size", "pk": 4, "fields": {"size": "l"}}, {"model": "shop.size", "pk": 5, "fields": {"size": "xxl"}}, {"model": "shop.size", "pk": 3, "fields": {"size": "xs"}}, {"model": "shop.size", "pk": 2, "fields": {"size": "s"}}, {"model": "shop.size", "pk": 1, "fields": {"size": "xl"}}]',
#         'Blue':
#             '[{"model": "shop.size", "pk": 6, "fields": {"size": "m"}}, {"model": "shop.size", "pk": 3, "fields": {"size": "xs"}}, {"model": "shop.size", "pk": 2, "fields": {"size": "s"}}]'
#     }}


def image_details(img):
    # Loading the image
    image = Image.open(img)
    print(" 1")
    newimg = Image.open(img)
    newimg = image.convert("RGB")
    name = image.filename
    formated = newimg.save(f"{name}-webp-image.webp")
    return formated


def to_dict(instance, fields=None, exclude=None):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(instance)]
    return data


def hurry(instock):
    if instock <= 15:
        return "low"
    else:
        return "high"


# function to get item details for quickview
def quickviewres(slug):
    product = Product.objects.get(slug=slug)
    productvrt = ProductVaraiant.objects.filter(product__slug=slug)
    # storing the required quickview attributes in f=variables
    title = product.title
    slug = product.slug
    desc = product.description
    image = product.image.url
    price = product.price
    discount = product.discount_price
    # creating a list for the attribute of color and size because it is a foreign key item
    color = []
    size = []

    for vrt in productvrt:
        color.append(vrt.color)
        size.append(vrt.size)
    print(type(color))
    print(f"{str(color)}__-__{str(size)}")
    # serializing the color and size attribute
    color = serializers.serialize("json", color, fields=("color", "name"))
    size = serializers.serialize("json", size, fields=("size"))
    # storing the attributes in the data dictionary and sending it as response
    data = {
        "title": title,
        "desc": desc,
        "slug": slug,
        "discount": discount,
        "price": price,
        "image": image,
        "color": color,
        "size": size,
    }
    return data


def instock(slug):
    vrt = ProductVaraiant.objects.filter(product__slug=slug).values()
    x = 0
    for vrt in vrt:
        x = x + vrt["amount_in_stock"]
    return x


# import csv

# from .models import Product

# def run(file):
#     open = open(file)
#     read = csv.reader(open)

#     Product.objects.all().delete()

#     for row in read:

#         product = Product.create(product=row[0],description=row[1], price=row[2])
#         product.save()

# # a function to generate sku for the e-store
# def sku_generator():
#     sku = "sku"
#     return sku

# a function to generate the product item details


def productitem(slug):
    product = Product.objects.get(slug=slug)
    productvrt = ProductVaraiant.objects.filter(product__slug=slug).all()

    # storing the required quickview attributes in variables
    title = product.title
    slug = product.slug
    desc = product.description
    category = product.category.title
    image = product.image.url
    price = product.price
    discount = None
    if product.discount_price:
        discount = product.discount_price

    # color = {}
    # size = []

    pvrt = {}

    # for vrt in productvrt:
    #     pvrt[vrt.color.name] = product_variant_serializer(
    #         "json", vrt.size.all())
    # for vrt in productvrt:
    #     pvrt[vrt.color.name] = to_dict(vrt.size.all())
    for vrt in productvrt:
        pvrt[vrt.color.name] = serializers.serialize(
            "json", vrt.size.all().only("size"), fields=("size")
        )

    item = {
        "product_title": title,
        "product_slug": slug,
        "product_desc": desc,
        "product_image": image,
        "product_price": price,
        "product_discount": discount,
        "product_category": category,
        "product_variant": pvrt,
    }

    print(item)
    return item


# productitem("19a9515d-c8c8-11ed-9b60-8b569fb40be2")
