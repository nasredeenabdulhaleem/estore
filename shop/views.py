import datetime
import json
from sys import getsizeof
from django.contrib import messages
from .pay import initializepay
from sqlite3 import DataError, DatabaseError, IntegrityError
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views.generic import ListView, View, DetailView
from django.http import HttpResponseRedirect, JsonResponse, HttpRequest, HttpResponse
from .models import (
    Address,
    Mostpopular,
    OrderHistory,
    Payment,
    OrderItem,
    Picture,
    Product,
    OrderItem,
    Order,
    ProductVaraiant,
    UserProfile,
    VendorOrder,
)
from .forms import AddressUpdateForm, UserUpdateForm
from . import forms
from django.forms.models import model_to_dict

# from django.core import serializers
from .scripts import hurry, instock, productitem, quickviewres
from django.conf import settings
from pinax.eventlog.models import log
# log(
#         user=request.user,
#         action="CREATED_FOO_WIDGET",
#         obj=foo,
#         extra={"title": foo.title},
#     )

# Create your views here.

# //////--------/////////////////////////////////------------------///////////////////
# //////////////////---------------Detail View----------------------//////////////////
# /////--------/////////////////////////////////------------------///////////////////
##HOMEVIEW
class HomeView(ListView):
    template_name = "home.html"

    def get(self, request):
        product = Product.objects.all()
        user = request.user
        popular = Mostpopular.objects.all()
        if user.is_authenticated == True:
            cartitems = OrderItem.objects.filter(user_id=request.user.id)
            total = 0
            for item in cartitems:
                total += item.quantity * item.product.product.price
            total_items = OrderItem.objects.filter(user=request.user).count()
            cart = OrderItem.objects.filter(user_id=request.user.id)
        else:
            cart = None
            cartitems = None
            total_items = None
            total = None

        ctx = {
            "product": product,
            "popular": popular,
            "total_items": total_items,
            "total": total,
            "cart": cart,
        }
        return render(request, self.template_name, context=ctx)


# //////--------/////////////////////////////////------------------///////////////////
# //////////////////---------------Quick View----------------------//////////////////
# /////--------/////////////////////////////////------------------///////////////////
# /////--------Function for quick view for popover in home page-----------///////////////////
def quickview(request):
    data = json.loads(request.body)
    slug = data["productId"]
    data = productitem(slug)
    return JsonResponse(data, safe=False)


# //////--------/////////////////////////////////------------------///////////////////
# //////////////////---------------Detail View----------------------//////////////////
# /////--------/////////////////////////////////------------------///////////////////
##DETAILVIEW
class DetailView(DetailView):
    template_name = "shop/detail.html"

    def get(self, request, slug, *args, **kwargs):
        product = Product.objects.get(slug=slug)
        image = Picture.objects.filter(product__slug=slug).all()
        productvrt = ProductVaraiant.objects.filter(product__slug=slug)
        in_stock = instock(slug)
        # instock = sum(productvrt.amount_in_stock)
        # instock = 0
        # for item in productvrt:
        #     total += (item.amount_in_stock)
        # h = hurry(instock)
        # color = Color.objects.filter(product__slug=slug).all()
        ctx = {
            "product": product,
            "images": image,
            "productvrt": productvrt,
            "instock": in_stock,
            # 'hurry': h
        }
        return render(request, self.template_name, context=ctx)


""" 
Create Profile
"""
##PROFILEVIEW
class Profile(LoginRequiredMixin, View):
    template_name = "profile.html"
    login_url = "/login/"
    redirect_field_name = "redirect_to"

    def get(self, request):
        user_detail = UserProfile.objects.filter(user_id=request.user.id).all()
        user_address = Address.objects.filter(user_id=request.user.id).all()
        context = {"user_detail": user_detail, "address": user_address}
        return render(request, self.template_name, context)


##PROFILECREATE


class CreateProfile(LoginRequiredMixin, View):
    model = UserProfile
    template_name = "profile-create.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        number = request.POST.get("number")
        shipping_address = request.POST.get("shipping_address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")
        user = request.user.id

        profile = self.model.objects.create(
            user_id=user,
            firstname=firstname,
            lastname=lastname,
            email=email,
            gender=gender,
            phone=number,
        )
        profile.save()
        address = Address.objects.create(
            user_id=user,
            shipping_address=shipping_address,
            country=country,
            city=city,
            state=state,
        )
        address.save()
        messages.success(request, "Profile Created Successfully")
        return redirect("store:profile")


###PROFILEUPDATE


class UpdateProfile(LoginRequiredMixin, View):
    template_name = "profile-update.html"

    def get(self, request):
        try:

            user = UserProfile.objects.get(user=request.user)
            address = Address.objects.get(user=request.user)

            address_form = AddressUpdateForm(instance=address)
            user_form = UserUpdateForm(instance=user)
            context = {"userform": user_form, "addressform": address_form}

            return render(request, self.template_name, context)
        except DatabaseError:
            messages.info(
                self.request,
                "You have not saved your profile Info Please do that below",
            )
            return redirect("store:profile-create")

    def post(self, request):
        user = request.user.id
        userdetail = UserProfile.objects.get(user=request.user)
        addressdetail = Address.objects.get(user=request.user)
        userform = UserUpdateForm(request.POST, instance=userdetail)
        addressform = AddressUpdateForm(request.POST, instance=addressdetail)
        if userform.is_valid:
            userdetail = userform.save(commit=False)
            userdetail.user_id = user  # The logged-in user
            userdetail.save()
            if addressform.is_valid:
                addressform.save()
                addressdetail = addressform.save(commit=False)
                addressdetail.user_id = user  # The logged-in user
                addressdetail.save()
                messages.info(request, "Your Profile was updated Successfully")
                return redirect("store:profile")
            else:
                messages.info(
                    request,
                    "There was an Error Updating Your Address Details, Please Try again Later",
                )
                return redirect("store:profile")
        else:
            messages.info(
                request,
                "There was an Error Updating Your User Details, Please Try again Later",
            )
            return redirect("store:profile")


# Cart View
class CartView(LoginRequiredMixin, ListView):
    model = OrderItem
    template_name = "cart.html"

    def get(self, request):
        cartitems = OrderItem.objects.filter(user_id=request.user.id)
        total = 0
        for item in cartitems:
            total += item.quantity * item.product.product.price
        total_items = self.model.objects.filter(user=request.user).count()
        cart = self.model.objects.filter(user_id=request.user.id)
        context = {"total_items": total_items, "total": total, "cart": cart}

        return render(request, self.template_name, context)


###CHECKOUTVIEW


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            address = Address.objects.get(user_id=request.user.id)
            form = AddressUpdateForm(instance=address)
            total_items = OrderItem.objects.filter(user=request.user).count()
            cart = OrderItem.objects.filter(user_id=request.user.id, ordered=False)
            order = Order.objects.filter(user=request.user)
            user = UserProfile(user_id=request.user.id)
            cartitems = OrderItem.objects.filter(user_id=request.user.id)
            total = 0
            for item in cartitems:
                total += item.quantity * item.product.product.price
            context = {
                "cart": cart,
                "form": form,
                "order": order,
                "total_items": total_items,
                "total": total,
            }
            return render(request, "checkout.html", context)
        except ObjectDoesNotExist:
            if OrderItem.objects.all() == None:
                messages.info(
                    request,
                    "You do not have an active order, Please add an item to your Cart",
                )
                return redirect("store:store")
            elif Address.objects.all() == None:
                messages.info(
                    request, "Please complete your shipping address Information"
                )
                return redirect("store:profile-create")

    def post(self, request):
        try:
            address = Address.objects.filter(pk=request.user.id).first()
            form = AddressUpdateForm(request.POST, instance=address)
            if not form.is_valid():
                context = {"form": form}
                return render(request, self.template_name, context)
            else:
                form.save()
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        except DatabaseError:
            messages.info(
                self.request, "Please complete your shipping address Information"
            )
            return redirect("store:profile-create")


@login_required
def makepayment(request):

    user = request.user
    order = Order.objects.get(user_id=user.id, ordered=False)
    cartitems = OrderItem.objects.filter(user_id=user.id)
    email = UserProfile.objects.get(user_id=user.id).email
    total = 0
    for item in cartitems:
        total += item.quantity * item.product.product.price
    payment = Payment.objects.create(amount=total, email=email, ref=order.ref)
    ref = payment.ref
    print(ref)
    response = initializepay(email, total, ref)
    print(response)
    if response["status"] == True:
        resdata = response["data"]
        redirect_url = resdata["authorization_url"]
        print(redirect_url)
        ref = resdata["reference"]
        access = resdata["access_code"]
        data = [{"status": "200"}, {"redirect_url": redirect_url}]
        return JsonResponse(data, safe=False)
    else:
        data = [{"status": "401"}]
        return JsonResponse(data, safe=False)


@login_required
def AddToCart(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            color = request.POST.get("color")
            size = request.POST.get("size")
            prodid = request.POST.get("prodid")
            qty = int(request.POST.get("quantity"))

            print(f"{color} {size} {prodid} {qty}")
            # data = json.loads(request.body)
            # print(data["form"].color)
            # for x in data["form"]:
            #     print(x)
            # slug = data["productId"]
            # action = data["action"]
            user = request.user

            product = ProductVaraiant.objects.get(
                product__slug=prodid, color_id=color, size_id=size
            )
            orderitem, created = OrderItem.objects.get_or_create(
                product=product, user=user, ordered=False
            )
            order_qs = Order.objects.filter(user=user, ordered=False)
            if order_qs.exists():
                order = order_qs.first()

                if order.items.filter(product__slug=product.slug).exists():
                    print("exists")
                    orderitem.quantity += qty
                    orderitem.save()
                    messages.info(request, "Item was added succesfully")
                    return redirect("store:cart")
                else:
                    order.items.add(orderitem)
                    orderitem.quantity += qty
                    orderitem.save()
                    messages.info(request, "Item was added succesfully")
                    return redirect("store:cart")

            else:
                ordered_date = datetime.datetime.now()
                order = Order.objects.create(
                    user=request.user, ordered_date=ordered_date
                )
                orderitem.quantity += qty
                order.items.add(orderitem)
                order.save()
                messages.info(request, "This item was added to your cart.")
                return redirect("store:cart")

            # return JsonResponse("item was added", safe=False)
        else:
            messages.info(request, "Your request couldn't be processed.")
            return redirect("store:store")
    else:
        return JsonResponse({"url": "accounts/login/"}, safe=False)


@login_required
def UpdateCart(request):

    data = json.loads(request.body)
    slug = data["productId"]
    action = data["action"]
    print(f"{action} {slug}")
    user = request.user
    product = ProductVaraiant.objects.get(slug=slug)
    print(product)
    orderitem, created = OrderItem.objects.get_or_create(
        product=product, user=user, ordered=False
    )
    order_qs = Order.objects.filter(user=user, ordered=False)
    if order_qs.exists():
        order = order_qs.first()
        if order.items.filter(product__slug=product.slug).exists():
            if action == "add":
                orderitem.quantity += 1
                orderitem.save()
            elif action == "reduce":
                orderitem.quantity -= 1
                orderitem.save()
            if orderitem.quantity <= 0:
                orderitem.delete()
        else:
            order.items.add(orderitem)
            orderitem.save()
    else:
        ordered_date = datetime.datetime.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(orderitem)
        messages.info(request, "This item was added to your cart.")
        order.save()
    return JsonResponse("item was added", safe=False)


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    OrderItem = OrderItem.objects.get_or_create(product=item)
    if OrderItem.objects.filter(product=item).exists():
        OrderItem.item.remove()
        OrderItem.save()
        order_query = Order.objects.filter(user=request.user, ordered=False)
        order = order_query
        order.add(OrderItem)
        order.save()
        messages.success(request, "item succsssfully removed")
    else:
        messages.error(request, "yay this item is not in your OrderItem")


###Making And Validating Payments
def initiate_payment(request):
    if request.method == "POST":
        payment_form = forms.PaymentForm(request.POST)
        if payment_form.is_valid():
            payment = payment_form.save()
            return render(
                request,
                "make_payment.html",
                {
                    "payment": payment,
                    "paystack_public_key": settings.PAYSTACK_PUBLIC_KEY,
                },
            )
    else:
        payment_form = forms.PaymentForm()
    return render(request, "initiate-payment.html", {"payment": payment_form})


def validate_payment(request):
    # body_unicode = request.body.decode('utf-8')
    # body = json.loads(body_unicode)
    # ref = body['reference']
    ref = request.GET.get("reference")
    print(ref)
    user = request.user
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        order = Order.objects.get(ref=ref)

        order_items = order.items.all()
        order_items.update(ordered=True)
        for item in order_items:
            item.save()
        order.ordered = True
        order.save(update_fields=["ordered"])
        order_history = OrderHistory.objects.create(user_id=user.id, order=order)
        order_history.save()
        messages.success(request, "Verification Successfull")
        return redirect(("store:reciept"), slug=ref)
    else:
        messages.error(request, "Verification Failed")
    return redirect("store:checkout")


def reciept(request, slug):
    ref = slug
    order = Order.objects.filter(ref=ref)
    ctx = {
        "order": order,
    }
    return render(request, "reciept.html", context=ctx)


###################################################################################################
######################################Vendor View Section########################################
###################################################################################################

# Vendor Dashboard View Section

class VendorHomeView(View):
    template_name = "vendor/store-front.html"

    def get(self, request):
        
        # order = VendorOrder.objects.filter(user_user_id=request.user.id)
        # context ={

        # }

        return render(request, self.template_name)

####################################################################################################3
########################################VENDORS SECTION################################################
####################################################################################################################################
# Vendor Dashboard

class VendorDashboardView(View):
    template_name = "vendor/dashboard.html"
    
    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)
    
# settings
def VendorSettings(request, *args, **kwargs):


    return render(request, "vendor/settings.html")

# Vendor Order

def VendorOrderView(request, *args, **kwargs):
    # order = VendorOrder.objects.filter(user_user_id=request.user.id)
    # context ={
    #     'order': order
    # }
    return render(request, "vendor/orders.html")

#Product View

class ProductView(View):
    template_name = "vendor/product.html"

    def get(self, request, *args, **kwargs):
        # product = Product.objects.filter(user_id=request.user.id)
        context ={
            # "product": product,
            "title": "product"
        }
        return render(request, self.template_name, context)

#Add product View

class AddProductView(View):

    template_name = "vendor/add-product.html"

    def get(self, request):
        # form = forms.AddProductForm()
        context = {
        #     "form": form,
        #     "category": category
            "title": "Add Product"
        }
        return render(request, self.template_name,context)

    def post(self, request):
        form = forms.AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            messages.success(request, "Product Added Successfully")
            return redirect("store:vendor-storefront")
        else:
            messages.error(request, "Error Adding Product")
            return redirect("store:vendor-storefront")
        

# Update Product

class UpdateProductView(View):

    template_name = "vendor/update-product.html"

    def get(self, request, *args,**kwargs):

        context = {
            "title": "Update Product"
        }
        return render(request, self.template_name, context)

# Delete Product
class DeleteProductView(View):

    template_name = "vendor/delete-product.html"

    def get(self, request, *args, **kwargs):

        context = {
            "title": "Delete Product"
        }
        return render(request, self.template_name, context)

# Vendor Customers

class VendorCustomersView(View):

    template_name = "vendor/customers.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    

