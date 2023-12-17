import datetime
import json
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from shop.vendorforms.addproduct import AddProductForm
from shop.vendorforms.productitem import (
    ProductItemForm,
    ProductItemFormVariation1,
    ProductItemFormVariation2,
    ProductItemFormVariation3,
)
from shop.globalcontext import user_context_processor
from .pay import initializepay
from sqlite3 import DatabaseError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views.generic import ListView, View, DetailView, UpdateView
from django.http import HttpResponseRedirect, JsonResponse

# from shop.forms.addproduct import AddProductForm
from .models import (
    Address,
    Cart,
    CartItem,
    Color,
    Mostpopular,
    OrderHistory,
    Payment,
    OrderItem,
    Picture,
    Product,
    OrderItem,
    Order,
    ProductItem,
    ProductVaraiant,
    Size,
    UserAddress,
    UserProfile,
    VendorProfile,
)
from .forms import (
    AddressForm,
    AddressUpdateForm,
    ProductAddToCartForm,
    ProductAddToCartFormV1,
    ProductAddToCartFormV3,
    ProductAddToCartFormV2,
    UserProfileForm,
)
from . import forms

# from django.core import serializers
from .scripts import productitem
from django.conf import settings
from django.views.generic import DeleteView, CreateView
from django.urls import reverse_lazy
from .models import Product

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
    template_name = "shop/index.html"

    def get(self, request):
        product = Product.objects.all()
        user = request.user
        popular = Mostpopular.objects.all()

        ctx = {
            "title": "Home Page",
            "Description": "",
            "products": product,
            "popular": popular,
        }
        ctx["data"] = user_context_processor(request)

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

    def get_form_class(self):
        slug = self.kwargs.get("slug")
        product = Product.objects.get(slug=slug)
        if product.variation.name == "Default":
            return ProductAddToCartFormV1
        elif product.variation.name == "Size":
            return ProductAddToCartFormV3
        elif product.variation.name == "Color":
            return ProductAddToCartFormV2
        else:
            return ProductAddToCartForm

    def get_context_data(self, slug):
        product = Product.objects.get(slug=slug)
        image = Picture.objects.filter(product__slug=slug).all()
        productitem = ProductItem.objects.filter(product__slug=slug)
        form_class = self.get_form_class()
        form = form_class(product_slug=slug)
        ctx = {
            "product": product,
            "images": image,
            "productitem": productitem,
            "form": form,
            "slug": slug,
            "data": user_context_processor(self.request),
        }
        return ctx

    def get(self, request, slug, *args, **kwargs):
        ctx = self.get_context_data(slug)
        return render(request, self.template_name, context=ctx)

    def post(self, request, slug, *args, **kwargs):
        user = request.user
        form_class = self.get_form_class()
        form = form_class(request.POST, product_slug=slug)
        if form.is_valid():
            quantity = form.cleaned_data["quantity"]

            productitem = (
                form.get_product_item()
            )  # ProductItem.get_by_color_and_size(color, size)

            # Get or create the cart for the current user
            cart, created = Cart.objects.get_or_create(user=user)

            # Get or create the cart item for the product
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=productitem
            )

            # If the cart item was just created, set the quantity
            if created:
                cart_item.quantity += quantity
                cart_item.save()
            else:
                cart_item.quantity += quantity
                cart_item.save()

            messages.success(request, "Product Added Successfully")
            return redirect("store:detail", slug=slug)
        else:
            ctx = self.get_context_data(slug)
            ctx["form"] = form  # Update form with the submitted one
            messages.error(request, "Error Adding Product")
            return render(request, self.template_name, ctx)


"""
Searh For Products View
"""


def search(request):
    query = request.GET.get("q")
    if query:
        results = Product.objects.filter(
            Q(title__icontains=query) | Q(category__category__icontains=query)
        )
    else:
        results = Product.objects.all()

    paginator = Paginator(results, 10)  # Show 10 products per page.
    page_number = request.GET.get("page")
    results = paginator.get_page(page_number)

    return render(request, "shop/search.html", {"results": results})


"""
User Settings
"""


def user_settings(request, *args, **kwargs):
    context = {
        "user": request.user,
        "data": user_context_processor(request),
    }
    return render(request, "shop/user/settings.html", context=context)


""" 
Create Profile
"""


##PROFILEVIEW
def Profile(request, *args, **kwargs):
    template_name = "shop/user/profile.html"
    try:
        user_profile = UserProfile.objects.get(user_id=request.user.id)
    except UserProfile.DoesNotExist:
        user_profile = False
    try:
        user_address = UserAddress.objects.get(user_id=request.user.id)
    except UserAddress.DoesNotExist:
        user_address = False
    context = {
        "user_profile": user_profile,
        "address": user_address,
        "data": user_context_processor(request),
    }

    return render(request, template_name, context)


##PROFILECREATE


class CreateProfile(LoginRequiredMixin, View):
    model = UserProfile
    template_name = "shop/user/create-profile.html"

    def get(self, request):
        form = UserProfileForm()

        context = {
            "form": form,
            "data": user_context_processor(request),
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user_id = request.user.id
            profile.save()
            messages.success(request, "Profile Created Successfully")
            return redirect("store:profile")
        else:
            context = {
                "form": form,
                "data": user_context_processor(request),
            }
            messages.error(request, "Error Creating Profile")
            return render(request, self.template_name, context)


###PROFILEUPDATE


class UpdateProfile(LoginRequiredMixin, View):
    template_name = "shop/user/update-profile.html"

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            messages.info(
                request, "You have not saved your profile Info Please do that below"
            )
            return redirect("store:create-profile")

        form = UserProfileForm(instance=user_profile)

        context = {
            "form": form,
            "data": user_context_processor(request),
        }

        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        userdetail = UserProfile.objects.get(user=user)

        form = UserProfileForm(request.POST, instance=userdetail)

        if form.is_valid:
            userdetail = form.save()
            # userdetail.user_id = user  # The logged-in user
            # userdetail.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect("store:profile")
        else:
            messages.error(
                request,
                "There was an Error Updating Your User Profile, Please Try Again",
            )
            context = {
                "form": form,
                "data": user_context_processor(request),
            }
            return render(request, self.template_name, context)


##AddressCREATE


class CreateAddress(LoginRequiredMixin, View):
    template_name = "shop/user/create-address.html"

    def get(self, request):
        form = AddressForm()

        context = {
            "form": form,
            "data": user_context_processor(request),
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user_id = request.user.id
            address.save()
            UserAddress.objects.create(user_id=request.user.id, address=address)
            messages.success(request, "Shipping Address Added Successfully")
            return redirect("store:profile")
        else:
            context = {
                "form": form,
                "data": user_context_processor(request),
            }
            messages.error(request, "Error Adding Shipping Address")
            return render(request, self.template_name, context)


###AddressUPDATE


class UpdateAddress(LoginRequiredMixin, View):
    template_name = "shop/user/update-address.html"

    def get(self, request):
        try:
            user_address = UserAddress.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            messages.info(
                request, "You have not added Your ShippingInfo Please do that below"
            )
            return redirect("store:create-address")

        form = AddressForm(instance=user_address.address)

        context = {
            "form": form,
            "data": user_context_processor(request),
        }

        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        useraddress = UserAddress.objects.get(user=user)

        form = AddressForm(request.POST, instance=useraddress.address)

        if form.is_valid:
            useraddress = form.save()
            # userdetail.user_id = user  # The logged-in user
            # userdetail.save()
            messages.success(request, "Shipping Address Updated Successfully")
            return redirect("store:profile")
        else:
            messages.error(
                request,
                "There was an Error Updating Your Shipping Address, Please Try Again",
            )
            context = {
                "form": form,
                "data": user_context_processor(request),
            }
            return render(request, self.template_name, context)


# Cart View
class CartView(LoginRequiredMixin, ListView):
    model = OrderItem
    template_name = "shop/cart.html"

    def get(self, request):
        cartitems = CartItem.objects.filter(cart__user=request.user)
        context = {
            "cart": cartitems,
            "data": user_context_processor(request),
        }

        return render(request, self.template_name, context)


# Increase item Quantity by one


def increaseItem(request, id):
    user = request.user
    # product = CartItem.objects.get(id=id)
    cart_qs = Cart.objects.filter(user=user)
    if cart_qs.exists():
        cart = cart_qs[0]
        # check if the order item is in the order
        cart_item = CartItem.objects.get(cart=cart, id=id)
        if cart_item.quantity < cart_item.product.quantity_in_stock:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.info(
                request,
                "You have reached the maximum quantity for this item, Item is now out of stock",
            )
    else:
        messages.info(request, "You do not have an active order")
    return redirect("store:cart")


# Decrease item Quantity by one
def decreaseItem(request, id):
    user = request.user
    # product = CartItem.objects.get(id=id)
    cart_qs = Cart.objects.filter(user=user)
    if cart_qs.exists():
        cart = cart_qs[0]
        # check if the order item is in the order
        cart_item = CartItem.objects.get(cart=cart, id=id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            messages.info(
                request, "You have reached the minimum quantity for this item"
            )
    else:
        messages.info(request, "You do not have an active order")
    return redirect("store:cart")


# Remove item from cart
def removeItem(request, id):
    user = request.user
    cart_qs = Cart.objects.filter(user=user)
    if cart_qs.exists():
        cart = cart_qs[0]
        # check if the order item is in the order
        cart_item = CartItem.objects.get(cart=cart, id=id)
        cart_item.delete()
    else:
        messages.info(request, "You do not have an active order")
    return redirect("store:cart")


###CHECKOUTVIEW


class CheckoutView(LoginRequiredMixin, View):
    template_name = "shop/checkout.html"

    def get(self, request):
        cartitems = CartItem.objects.filter(cart__user=request.user)
        context = {
            "cart": cartitems,
            "data": user_context_processor(request),
        }
        try:
            user_address = get_object_or_404(UserAddress, user=request.user)
            context["address"] = user_address
        except Http404:
            context["address"] = False
        return render(request, self.template_name, context)

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


@login_required  # type: ignore
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


# Product View


class ProductView(View):
    template_name = "vendor/product.html"

    def get(self, request, *args, **kwargs):
        product = Product.objects.filter(vendor__user=request.user).all()
        context = {"products": product, "title": "product"}
        return render(request, self.template_name, context)


# A view to show a detail of a vendor product
def vendor_product_detail(request, slug, *args, **kwargs):
    product = Product.objects.get(vendor__user=request.user, slug=slug)
    productitem = ProductItem.objects.filter(product=product)
    context = {
        "product": product,
        "productitem": productitem,
        "title": "Product Details",
    }
    return render(request, "vendor/product-detail.html", context)


# Add product View


class AddProductView(View):
    template_name = "vendor/add-product.html"

    def get(self, request):
        form = AddProductForm()
        context = {
            "form": form,
            # "category": category
            "title": "Add Product",
        }
        return render(request, self.template_name, context)

    def post(self, request):
        vendor = VendorProfile.objects.get(user_id=request.user.id)
        form = AddProductForm(request.POST, request.FILES)
        context = {
            "form": form,
            "title": "Add Product",
        }
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = vendor
            product.save()

            product_variation = form.cleaned_data.get("variation")
            if product_variation.name == "Default":
                default_color = Color.objects.get(name="Default")
                default_size = Size.objects.get(title="Default")
                ProductItem.objects.create(
                    product=product,
                    quantity_in_stock=1,
                    description=product.description,
                    product_image=product.image.url,
                    color=default_color,
                    size=default_size,
                    price=product.price,
                )

            messages.success(request, "Product Added Successfully")
            return redirect("store:vendor_product_detail", slug=product.slug)
        else:
            messages.error(request, "Error Adding Product")
            return render(request, self.template_name, context)


# Update Product


class UpdateProductView(UpdateView):
    template_name = "vendor/update-product.html"
    model = Product
    form_class = AddProductForm

    def get_queryset(self):
        return self.model.objects.filter(
            vendor__user=self.request.user, slug=self.kwargs["slug"]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Product"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Product updated successfully")
        return super().form_valid(form)

    # def get(self, request,slug, *args, **kwargs):
    #     product = Product.objects.get(vendor__user=request.user, slug=slug)
    #     form = AddProductForm(instance=product)
    #     context = {
    #         "form": form,
    #         "title": "Update Product",
    #     }
    #     return render(request, self.template_name, context)


# Delete Product


class DeleteProductView(DeleteView):
    template_name = "vendor/delete-product.html"
    model = Product
    success_url = reverse_lazy("store:vendor-products")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Product deleted successfully")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Product"
        return context


##Product Item

# Add product item


class AddProductItemView(CreateView):
    model = ProductItem
    # form_class = ProductItemForm
    template_name = "vendor/add-product-item.html"

    # success_url = reverse_lazy('store:vendor_product_detail')
    def get_success_url(self):
        return reverse_lazy(
            "store:vendor_product_detail", kwargs={"slug": self.kwargs.get("slug")}
        )

    def get_form_class(self):
        product_slug = self.kwargs.get("slug")
        product = Product.objects.get(slug=product_slug)
        if product.variation.name == "Default":
            return ProductItemFormVariation1
        elif product.variation.name == "Size":
            return ProductItemFormVariation2
        elif product.variation.name == "Color":
            return ProductItemFormVariation3
        else:
            return ProductItemForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        product_slug = self.kwargs.get("slug")
        product = Product.objects.get(slug=product_slug)

        if product.variation.name == "Default":
            # For ProductItemFormVariation1, set initial values for color and size
            kwargs["initial"]["color"] = Color.objects.get(name="Default")
            kwargs["initial"]["size"] = Size.objects.get(title="Default")
        elif product.variation.name == "Size":
            # For ProductItemFormVariation2, set initial value for color
            kwargs["initial"]["color"] = Color.objects.get(name="Default")
        elif product.variation.name == "Color":
            # For ProductItemFormVariation3, set initial value for size
            kwargs["initial"]["size"] = Size.objects.get(title="Default")

        # Set initial value for the product field
        kwargs["initial"]["product"] = product

        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            messages.success(self.request, "Product item added successfully")
            return super().form_valid(form)
        else:
            print(form.errors)
            return self.form_invalid(form)

    def form_invalid(self, form):
        kwargs = super().get_form_kwargs()
        product_slug = self.kwargs.get("slug")
        product = Product.objects.get(slug=product_slug)
        form.initial["product"] = "default_value"
        if product.variation.name == "Default":
            # For ProductItemFormVariation1, set initial values for color and size
            form.initial["color"] = Color.objects.get(name="Default")
            form.initial["size"] = Size.objects.get(title="Default")
        elif product.variation.name == "Size":
            # For ProductItemFormVariation2, set initial value for color
            form.initial["color"] = Color.objects.get(name="Default")
        elif product.variation.name == "Color":
            # For ProductItemFormVariation3, set initial value for size
            form.initial["size"] = Size.objects.get(title="Default")

        # Set initial value for the product field
        form.initial["product"] = product

        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Product Item"
        product_slug = self.kwargs.get("slug")
        product = Product.objects.get(slug=product_slug)
        context["product"] = product
        return context


# Update Product
class UpdateProductItemView(UpdateView):
    model = ProductItem
    form_class = ProductItemForm
    template_name = "vendor/update-product-item.html"

    def get_form_class(self):
        product = self.object.product  # type: ignore
        if product.variation.name == "Default":
            return ProductItemFormVariation1
        elif product.variation.name == "Size":
            return ProductItemFormVariation2
        elif product.variation.name == "Color":
            return ProductItemFormVariation3
        else:
            return ProductItemForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # product_slug = self.kwargs.get("slug")
        product = Product.objects.get(slug=self.object.product.slug)  # type: ignore Product.objects.get(slug=product_slug)

        if product.variation.name == "Default":
            # For ProductItemFormVariation1, set initial values for color and size
            kwargs["initial"]["color"] = Color.objects.get(name="Default")
            kwargs["initial"]["size"] = Size.objects.get(title="Default")
        elif product.variation.name == "Size":
            # For ProductItemFormVariation2, set initial value for color
            kwargs["initial"]["color"] = Color.objects.get(name="Default")
        elif product.variation.name == "Color":
            # For ProductItemFormVariation3, set initial value for size
            kwargs["initial"]["size"] = Size.objects.get(title="Default")

        # Set initial value for the product field
        kwargs["initial"]["product"] = product
        # print(kwargs)
        return kwargs

    # def get_queryset(self):
    #     return self.model.objects.filter(
    #         product__vendor__user=self.request.user, pk=self.kwargs["pk"]
    #     )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Product"
        is_update = self.object is not None  # type: ignore
        context["is_update"] = is_update

        return context

    def get_success_url(self):
        return reverse_lazy(
            "store:vendor_product_detail", kwargs={"slug": self.object.product.slug}  # type: ignore
        )

    def get_initial(self):
        initial = super().get_initial()
        product = Product.objects.get(slug=self.object.product.slug)  # type: ignore
        initial["product"] = product
        return initial

    def form_valid(self, form):
        messages.success(self.request, "Product item updated successfully")
        return super().form_valid(form)


class DeleteProductItemView(DeleteView):
    model = ProductItem
    template_name = "vendor/delete_productitem.html"

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Product item deleted successfully")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            "store:vendor_product_detail", kwargs={"slug": self.object.product.slug}  # type: ignore
        )


# Vendor Customers


class VendorCustomersView(View):
    template_name = "vendor/customers.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
