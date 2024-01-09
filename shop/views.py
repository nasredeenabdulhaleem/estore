import json
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.utils.html import mark_safe
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.db.models import Q
from markdown import markdown
from shop.utils.utils import generate_order_id, user_passes_test_with_args
from shop.vendorforms.addproduct import AddProductForm
from shop.vendorforms.productitem import (
    ProductItemForm,
    ProductItemFormVariation1,
    ProductItemFormVariation2,
    ProductItemFormVariation3,
)
from shop.globalcontext import user_context_processor, vendor_context_processor
from .pay import initializepay
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render, get_list_or_404
from django.contrib import messages
from django.views.generic import ListView, View, DetailView, UpdateView
from django.http import BadHeaderError, Http404, HttpResponse, JsonResponse
from django.core.mail import send_mail

from django.http import FileResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO


from .models import (
    Address,
    Cart,
    CartItem,
    Color,
    Country,
    Mostpopular,
    OrderHistory,
    OrderStatus,
    Payment,
    OrderItem,
    Picture,
    Product,
    OrderItem,
    Order,
    ProductItem,
    Size,
    UserAddress,
    UserProfile,
    VendorProfile,
    VendorStore,
)
from .forms import (
    AddressForm,
    CheckoutForm,
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
from django.urls import reverse, reverse_lazy
from .models import Product
from accounts.models import User

# log(
#         user=request.user,
#         action="CREATED_FOO_WIDGET",
#         obj=foo,
#         extra={"title": foo.title},
#     )


# Create your views here.
def business_name_exists(business_name):
    return VendorProfile.objects.filter(business_name=business_name).exists()


def is_store_admin(business_name, user) -> bool:
    vendor = VendorProfile.objects.get(user=user).business_name
    return vendor == business_name


def is_user(user):
    return user.is_authenticated and user.role == "User"


def is_vendor(user, business_name):
    return (
        user.is_authenticated
        and user.role == "Vendor"
        and is_store_admin(business_name, user)
    )
    # return user.is_authenticated and user.role == "Vendor"


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


@login_required
@user_passes_test(is_user, login_url=reverse_lazy("login"))
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
@login_required
@user_passes_test(is_user, login_url=reverse_lazy("login"))
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


class CreateProfile(LoginRequiredMixin, UserPassesTestMixin, View):
    model = UserProfile
    template_name = "shop/user/create-profile.html"

    def test_func(self):
        return is_user(self.request.user)

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


class UpdateProfile(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "shop/user/update-profile.html"

    def test_func(self):
        return is_user(self.request.user)

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


class CreateAddress(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "shop/user/create-address.html"

    def test_func(self):
        return is_user(self.request.user)

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


class UpdateAddress(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "shop/user/update-address.html"

    def test_func(self):
        return is_user(self.request.user)

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
class CartView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = OrderItem
    template_name = "shop/cart.html"

    def test_func(self):
        return is_user(self.request.user)

    def get(self, request):
        cartitems = CartItem.objects.filter(cart__user=request.user)
        context = {
            "cart": cartitems,
            "data": user_context_processor(request),
        }

        return render(request, self.template_name, context)


# Increase item Quantity by one


@login_required
@user_passes_test(is_user, login_url=reverse_lazy("login"))
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
@login_required
@user_passes_test(is_user, login_url=reverse_lazy("login"))
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
@login_required
@user_passes_test(is_user, login_url=reverse_lazy("login"))
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


# class CheckoutView(LoginRequiredMixin, View):
#     template_name = "shop/checkout.html"

#     def get(self, request):
#         cartitems = CartItem.objects.filter(cart__user=request.user)
#         context = {
#             "cart": cartitems,
#             "data": user_context_processor(request),
#         }
#         try:
#             user_address = get_object_or_404(UserAddress, user=request.user)
#             context["address"] = user_address
#         except Http404:
#             context["address"] = False
#         return render(request, self.template_name, context)

#     def post(self, request):
#         try:
#             address = Address.objects.filter(pk=request.user.id).first()
#             form = AddressUpdateForm(request.POST, instance=address)
#             if not form.is_valid():
#                 context = {"form": form}
#                 return render(request, self.template_name, context)
#             else:
#                 form.save()
#             return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
#         except DatabaseError:
#             messages.info(
#                 self.request, "Please complete your shipping address Information"
#             )
#             return redirect("store:profile-create")


class CheckoutView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    View class for handling the checkout process.

    GET request:
    - Retrieves the user's cart items and displays the checkout form.
    - If the user has a saved address, the form is pre-filled with the address details.

    POST request:
    - Validates the submitted form data.
    - Creates an order and saves the address details if the form is valid.
    - Removes the purchased items from the user's cart.
    - Redirects to the order completion page.

    Attributes:
    - template_name (str): The name of the template used for rendering the checkout page.
    """

    template_name = "shop/checkout.html"

    def test_func(self):
        return is_user(self.request.user)

    def get(self, request):
        """
        Handles the GET request for the checkout page.

        Retrieves the user's cart items and displays the checkout form.
        If the user has a saved address, the form is pre-filled with the address details.

        Args:
        - request (HttpRequest): The HTTP request object.

        Returns:
        - HttpResponse: The HTTP response object containing the rendered checkout page.
        """
        cartitems = CartItem.objects.filter(cart__user=request.user)
        # check if an address instance exist for the user if it does exist initialize the form with the values
        try:
            user_address = get_object_or_404(UserAddress, user=request.user)
            form = CheckoutForm(
                initial={
                    "first_name": user_address.address.first_name,
                    "last_name": user_address.address.last_name,
                    "email": user_address.address.email,
                    "phone_number": user_address.address.phone_number,
                    "shipping_address": user_address.address.shipping_address,
                    "billing_address": user_address.address.billing_address,
                    "city": user_address.address.city,
                    "state": user_address.address.state,
                    "postal_code": user_address.address.postal_code,
                    "country": user_address.address.country,
                    "save_info": user_address.is_default,
                }
            )
        except Http404:
            form = CheckoutForm()
        context = {
            "form": form,
            "cart": cartitems,
            "data": user_context_processor(request),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        """
        Handles the POST request for the checkout page.

        Validates the submitted form data.
        Creates an order and saves the address details if the form is valid.
        Removes the purchased items from the user's cart.
        Redirects to the order completion page.

        Args:
        - request (HttpRequest): The HTTP request object.

        Returns:
        - HttpResponse: The HTTP response object for redirecting to the order completion page
                        or rendering the checkout page with form errors.
        """
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                user_address = get_object_or_404(UserAddress, user=request.user)
            except Http404:
                user_address = None
            if user_address:
                address = user_address.address
            else:
                country_data = form.cleaned_data["country_name"]
                country = Country.objects.get(country_name=country_data)
                address = Address.objects.create(
                    first_name=form.cleaned_data["first_name"],
                    last_name=form.cleaned_data["last_name"],
                    email=form.cleaned_data["email"],
                    phone_number=form.cleaned_data["phone_number"],
                    shipping_address=form.cleaned_data["shipping_address"],
                    billing_address=form.cleaned_data["billing_address"],
                    city=form.cleaned_data["city"],
                    state=form.cleaned_data["state"],
                    postal_code=form.cleaned_data["postal_code"],
                    country=country,
                )

            status = OrderStatus.objects.get(status="Awaiting Payment")
            order = Order.objects.create(
                user=request.user,
                ref=generate_order_id(),
                # Add other order fields here
                status=status,
                shipping_address=address,
            )

            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
            for cart_item in cart_items:
                OrderItem.objects.create(
                    user=request.user,
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                )
                cart.products.remove(cart_item.product)

            order.save()
            cart.save()

            if form.cleaned_data.get("save_info"):
                if user_address:
                    user_address.address = address
                    user_address.save()
                else:
                    UserAddress.objects.create(user=request.user, address=address)
            # messages.success("Checkou")
            return redirect(
                "store:complete_order", order_ref=order.ref
            )  # Redirect to the payment page

        context = {"form": form}
        return render(request, self.template_name, context)


class CompleteOrderView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "shop/complete-order.html"

    def test_func(self):
        return is_user(self.request.user)

    def get(self, request, *args, **kwargs):
        order_id = kwargs.get("order_ref")
        order = Order.objects.get(ref=order_id)
        order_items = OrderItem.objects.filter(order=order)
        user_address = UserAddress.objects.get(user=order.user)
        total = OrderItem.get_total_order_price(order=order)

        context = {
            "order": order,
            "order_items": order_items,
            "user_address": user_address,
            "data": user_context_processor(request),
            "total": total,
        }
        return render(request, self.template_name, context)


class OrderSummaryPDFView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return is_user(self.request.user)

    def get(self, request, *args, **kwargs):
        # Get the order
        order_ref = kwargs.get("order_ref")
        order = Order.objects.get(ref=order_ref)
        user_address = UserAddress.objects.get(user=order.user)
        total = OrderItem.get_total_order_price(order=order)

        # Render the template with context
        template = get_template("shop/order_summary.html")
        context = {
            "order": order,
            "order_items": OrderItem.objects.filter(order=order),
            "user_address": user_address,
            "total": total,
        }
        html = template.render(context)

        # Convert the HTML to PDF
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            return FileResponse(
                BytesIO(result.getvalue()), content_type="application/pdf"
            )

        return None


@login_required
@user_passes_test(is_user, login_url=reverse_lazy("login"))
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


# @login_required
# @user_passes_test(is_user,login_url= reverse_lazy("login"))
# def AddToCart(request):
#     if request.user.is_authenticated:
#         if request.method == "POST":
#             color = request.POST.get("color")
#             size = request.POST.get("size")
#             prodid = request.POST.get("prodid")
#             qty = int(request.POST.get("quantity"))

#             print(f"{color} {size} {prodid} {qty}")
#             # data = json.loads(request.body)
#             # print(data["form"].color)
#             # for x in data["form"]:
#             #     print(x)
#             # slug = data["productId"]
#             # action = data["action"]
#             user = request.user

#             product = ProductVaraiant.objects.get(
#                 product__slug=prodid, color_id=color, size_id=size
#             )
#             orderitem, created = OrderItem.objects.get_or_create(
#                 product=product, user=user, ordered=False
#             )
#             order_qs = Order.objects.filter(user=user, ordered=False)
#             if order_qs.exists():
#                 order = order_qs.first()

#                 if order.items.filter(product__slug=product.slug).exists():
#                     print("exists")
#                     orderitem.quantity += qty
#                     orderitem.save()
#                     messages.info(request, "Item was added succesfully")
#                     return redirect("store:cart")
#                 else:
#                     order.items.add(orderitem)
#                     orderitem.quantity += qty
#                     orderitem.save()
#                     messages.info(request, "Item was added succesfully")
#                     return redirect("store:cart")

#             else:
#                 ordered_date = datetime.datetime.now()
#                 order = Order.objects.create(
#                     user=request.user, ordered_date=ordered_date
#                 )
#                 orderitem.quantity += qty
#                 order.items.add(orderitem)
#                 order.save()
#                 messages.info(request, "This item was added to your cart.")
#                 return redirect("store:cart")

#             # return JsonResponse("item was added", safe=False)
#         else:
#             messages.info(request, "Your request couldn't be processed.")
#             return redirect("store:store")
#     else:
#         return JsonResponse({"url": "accounts/login/"}, safe=False)


# @login_required
# @user_passes_test(is_user, login_url=reverse_lazy("login"))
# def UpdateCart(request):
#     data = json.loads(request.body)
#     slug = data["productId"]
#     action = data["action"]
#     print(f"{action} {slug}")
#     user = request.user
#     product = ProductVaraiant.objects.get(slug=slug)
#     print(product)
#     orderitem, created = OrderItem.objects.get_or_create(
#         product=product, user=user, ordered=False
#     )
#     order_qs = Order.objects.filter(user=user, ordered=False)
#     if order_qs.exists():
#         order = order_qs.first()
#         if order.items.filter(product__slug=product.slug).exists():
#             if action == "add":
#                 orderitem.quantity += 1
#                 orderitem.save()
#             elif action == "reduce":
#                 orderitem.quantity -= 1
#                 orderitem.save()
#             if orderitem.quantity <= 0:
#                 orderitem.delete()
#         else:
#             order.items.add(orderitem)
#             orderitem.save()
#     else:
#         ordered_date = datetime.datetime.now()
#         order = Order.objects.create(user=request.user, ordered_date=ordered_date)
#         order.items.add(orderitem)
#         messages.info(request, "This item was added to your cart.")
#         order.save()
#     return JsonResponse("item was added", safe=False)


# @login_required  # type: ignore
# @user_passes_test(is_user, login_url=reverse_lazy("login"))
# def remove_from_cart(request, pk):
#     item = get_object_or_404(Product, pk=pk)
#     OrderItem = OrderItem.objects.get_or_create(product=item)
#     if OrderItem.objects.filter(product=item).exists():
#         OrderItem.item.remove()
#         OrderItem.save()
#         order_query = Order.objects.filter(user=request.user, ordered=False)
#         order = order_query
#         order.add(OrderItem)
#         order.save()
#         messages.success(request, "item succsssfully removed")
#     else:
#         messages.error(request, "yay this item is not in your OrderItem")


###Making And Validating Payments
@login_required
@user_passes_test(is_user, login_url=reverse_lazy("login"))
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


class VendorHomeView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "vendor/store-front.html"

    def test_func(self):
        return is_vendor(self.request.user)

    def get(self, request, slug):
        vendor_info = VendorStore.objects.get(store_name=slug)
        vendor_products = Product.objects.filter(vendor=vendor_info.vendor)

        # order = VendorOrder.objects.filter(user_user_id=request.user.id)
        context = {
            "vendor_products": vendor_products,
            "vendor_info": vendor_info,
            "data": user_context_processor(request),
        }

        return render(request, self.template_name, context)


####################################################################################################3
########################################VENDORS SECTION################################################
####################################################################################################################################
# Vendor Dashboard


class VendorDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "vendor/dashboard.html"

    def test_func(self):
        return is_vendor(
            self.request.user, self.kwargs["business_name"]
        ) and business_name_exists(self.kwargs["business_name"])

    def get_login_url(self):
        return reverse("vendor_login", args=[self.kwargs["business_name"]])

    def get(self, request, *args, **kwargs):
        context = {
            "business_name": vendor_context_processor(request),
        }
        return render(request, self.template_name, context=context)


# settings
@login_required
@user_passes_test_with_args(is_vendor, login_url=reverse_lazy("vendor_login"))
def VendorSettings(request, business_name, *args, **kwargs):
    context = {"business_name": business_name}
    return render(request, "vendor/settings.html", context=context)


# Vendor Order


@login_required
@user_passes_test_with_args(is_vendor, login_url=reverse_lazy("vendor_login"))
def VendorOrderView(request, business_name, *args, **kwargs):
    # order = VendorOrder.objects.filter(user_user_id=request.user.id)
    context = {
        # 'order': order,
        "business_name": business_name
    }
    return render(request, "vendor/orders.html", context=context)


class SearchOrdersView(LoginRequiredMixin, UserProfile, View):
    template_name = "orders/search.html"

    def test_func(self):
        return is_user(self.request.user) and business_name_exists(
            self.kwargs["business_name"]
        )

    def get(self, request):
        query = request.GET.get("q", "")
        status = request.GET.get("status", "")
        sort = request.GET.get("sort", "order_id")  # Default sort field is 'order_id'

        if status:
            orders = Order.objects.filter(
                Q(order_id__icontains=query) | Q(customer__name__icontains=query),
                status=status,
            )
        else:
            orders = Order.objects.filter(
                Q(order_id__icontains=query) | Q(customer__name__icontains=query)
            )

        orders = orders.order_by(sort)  # Sort the queryset

        return render(request, self.template_name, {"orders": orders})


# Product View


class ProductView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "vendor/product.html"

    def test_func(self):
        return is_vendor(
            self.request.user, self.kwargs["business_name"]
        ) and business_name_exists(self.kwargs["business_name"])

    def get(self, request, business_name, *args, **kwargs):
        product = Product.objects.filter(vendor__user=request.user).all()
        context = {
            "products": product,
            "title": "product",
            "business_name": business_name,
        }

        return render(request, self.template_name, context)


# A view to show a detail of a vendor product
@login_required
@user_passes_test_with_args(is_vendor, login_url=reverse_lazy("vendor_login"))
def vendor_product_detail(request, business_name, slug, *args, **kwargs):
    product = Product.objects.get(vendor__user=request.user, slug=slug)
    productitem = ProductItem.objects.filter(product=product)
    context = {
        "product": product,
        "productitem": productitem,
        "title": "Product Details",
        "business_name": business_name,
    }
    return render(request, "vendor/product-detail.html", context)


# Add product View


class AddProductView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "vendor/add-product.html"

    def test_func(self):
        return is_vendor(
            self.request.user, self.kwargs["business_name"]
        ) and business_name_exists(self.kwargs["business_name"])

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


class UpdateProductView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "vendor/update-product.html"
    model = Product
    form_class = AddProductForm

    def test_func(self):
        return is_vendor(
            self.request.user, self.kwargs["business_name"]
        ) and business_name_exists(self.kwargs["business_name"])

    def get_queryset(self):
        return self.model.objects.filter(
            vendor__user=self.request.user, slug=self.kwargs["slug"]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Product"
        context["business_name"] = self.kwargs["business_name"]
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


class DeleteProductView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "vendor/delete-product.html"
    model = Product
    success_url = reverse_lazy("store:vendor-products")

    def test_func(self):
        return is_vendor(
            self.request.user, self.kwargs["business_name"]
        ) and business_name_exists(self.kwargs["business_name"])

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Product deleted successfully")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Product"
        context["business_name"] = self.kwargs["business_name"]
        return context


##Product Item

# Add product item


class AddProductItemView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ProductItem
    # form_class = ProductItemForm
    template_name = "vendor/add-product-item.html"

    def test_func(self):
        return is_vendor(
            self.request.user, self.kwargs["business_name"]
        ) and business_name_exists(self.kwargs["business_name"])

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
        context["business_name"] = self.kwargs["business_name"]
        return context


# Update Product
class UpdateProductItemView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ProductItem
    form_class = ProductItemForm
    template_name = "vendor/update-product-item.html"

    def test_func(self):
        return is_vendor(
            self.request.user, self.kwargs["business_name"]
        ) and business_name_exists(self.kwargs["business_name"])

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
        context["business_name"] = self.kwargs["business_name"]

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


class DeleteProductItemView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ProductItem
    template_name = "vendor/delete_productitem.html"

    def test_func(self):
        return is_vendor(
            self.request.user, self.kwargs["business_name"]
        ) and business_name_exists(self.kwargs["business_name"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["business_name"] = self.kwargs["business_name"]
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Product item deleted successfully")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            "store:vendor_product_detail", kwargs={"slug": self.object.product.slug}  # type: ignore
        )


# Vendor Customers


class VendorCustomersView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "vendor/customers.html"

    def test_func(self):
        return is_vendor(
            self.request.user, self.kwargs["business_name"]
        ) and business_name_exists(self.kwargs["business_name"])

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


###################################################################################################3
########################################ERRORS VIEW SECTION################################################
####################################################################################################################################
#


def view_404(request, exception):
    return render(request, "404.html")


def view_500(request):
    return render(request, "500.html", status=500)


def view_403(request, exception):
    return render(request, "403.html", status=403)


def view_302(request, exception):
    return render(request, "302.html", status=302)


def view_400(request, exception):
    return render(request, "400.html", status=400)


###################################################################################################3
########################################Send mails SECTION################################################
####################################################################################################################################
# Send Mail


# 4173 9600 5411 9308


# def send_email_to_vendors(request):
#     if request.method == "POST":
#         vendors = get_list_or_404(User, role="vendor")
#         subject = request.POST.get("subject")
#         markdown_content = request.POST.get("markdown_content")
#         html_content = mark_safe(markdown(markdown_content))
#         text_content = "This is a message for vendors."

#         for vendor in vendors:
#             msg = EmailMultiAlternatives(subject, text_content, to=[vendor.email])
#             msg.attach_alternative(html_content, "text/html")
#             msg.send()

#         messages.info(request, "Emails sent to vendors.")
#         return redirect("store:vendor-mail")
#     else:
#         return render(request, "admin/send_email_to_vendors.html")
#     # if request.method == "POST":
#     #     try:
#     #         vendors = User.objects.filter(
#     #             role="vendor"
#     #         )  # Assuming 'role' field in User model
#     #         subject = request.POST.get("subject")  # Get subject from request
#     #         markdown_content = request.POST.get(
#     #             "markdown_content"
#     #         )  # Get markdown content from request
#     #         html_content = markdown.markdown(
#     #             markdown_content
#     #         )  # Convert markdown to HTML
#     #         email_content = render_to_string(html_content)
#     #         for vendor in vendors:
#     #             send_mail(
#     #                 subject=subject,
#     #                 message="This is a message for vendors.",
#     #                 recipient_list=[vendor.email],
#     #                 # fail_silently=False,
#     #                 html_message=email_content,
#     #             )
#     #         messages.info(request, "Emails sent to vendors.")
#     #         return redirect("store:vendor-mail")
#     #     except User.DoesNotExist:
#     #         messages.info(request, "No vendors found.")
#     #         return redirect("store:vendor-mail")
#     #     except BadHeaderError:
#     #         messages.info(request, "Invalid header found.")
#     #         return redirect("store:vendor-mail")
#     #     # except MarkdownError:
#     #     #     messages.info(request,"Error processing markdown.")
#     #     #     return redirect("store:vendor-mail")
#     #     except Exception as e:
#     #         messages.info(request, f"An error occurred: {str(e)}")
#     #         return redirect("store:vendor-mail")
#     # else:
#     #     return render(request, "admin/send_email_to_vendors.html")

# from django.template.loader import render_to_string


def send_email_to_vendors(request):
    if request.method == "POST":
        vendors = User.objects.filter(role="vendor")
        subject = request.POST.get("subject")
        markdown_content = request.POST.get("markdown_content")
        print(markdown_content)
        html_content = mark_safe(markdown(markdown_content))

        for vendor in vendors:
            context = {
                "subject": subject,
                "message": html_content,
                "vendor": vendor,
            }
            email_html_message = render_to_string(
                "emails/send-vendor-email.html", context
            )
            email_text_message = "This is a message for vendors."

            msg = EmailMultiAlternatives(subject, email_text_message, to=[vendor.email])
            msg.attach_alternative(email_html_message, "text/html")
            msg.send()

            send_mail(
                subject=subject,
                message=email_text_message,
                recipient_list=[vendor.email],
                html_message=email_html_message,
            )

        messages.info(request, "Emails sent to vendors.")
        return redirect("store:vendor-mail")
    else:
        return render(request, "admin/send_email_to_vendors.html")


def send_email_to_users(request):
    users = User.objects.filter(role="user")  # Assuming 'role' field in User model
    for user in users:
        send_mail(
            "Hello User",
            "This is a message for users.",
            "from@example.com",
            [user.email],
            fail_silently=False,
        )
    return HttpResponse("Emails sent to users.")
