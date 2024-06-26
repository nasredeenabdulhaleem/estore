import datetime
import email
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import User, VerificationCount
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.views import LoginView
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from shop.models import VendorProfile, VendorStore
from store import settings
from accounts.forms import SignupForm, LoginForm, VendorSignupForm
from pinax.eventlog.models import log
from accounts.emailverification import EmailVerification
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from accounts.emailverification import EmailVerification


# log(
#         user=request.user,
#         action="CREATED_FOO_WIDGET",
#         obj=foo,
#         extra={"title": foo.title},
#     )
# Create your views here.
def is_vendor(user):
    return user.is_authenticated and user.role == "Vendor"
    # return user.is_authenticated and user.role == "Vendor"


# USer SIGN UP View
class UserSignup(View):
    template_name = "accounts/user-signup.html"
    # form = UserCreationForm()

    def get(self, request):
        form = SignupForm()
        vendor_form = VendorSignupForm()
        context = {
            "form": form,
            "vendor_form": vendor_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = SignupForm(request.POST)
        vendor_form = VendorSignupForm()
        if form.is_valid():
            try:
                user = form.save()
                verification = VerificationCount.objects.create(
                    user=user, email=user.email, count=1
                )

                # email_verification = EmailVerification()
                # # Generate token and send verification email
                # # Generate token and send verification email
                # token = email_verification.generate_token(user.email)
                # email_sent = email_verification.send_verification_email(user)
                # log(
                #     user=user,
                #     action="Created a User Account, Verification Email Sent",
                #     obj=user,
                #     # extra={"title": foo.title},
                #     dateof=datetime.datetime.now(),
                # )
                messages.info(
                    request,
                    f"Created User {user.username}, a verification email has been sent to activate account",
                )
                return redirect("login")
            except Exception as e:
                print(e)
                messages.error(request, f"Error Creating Account, try again later")
                return render(request, self.template_name, {"form": form, "vendor_form": vendor_form})
        else:
            messages.error(request, f"Error Creating Account, Rectify error and retry")
            return render(request, self.template_name, {"form": form, "vendor_form": vendor_form})


class VerifyEmailView(View):
    """
    View to handle email verification.
    """

    def get(self, request, token):
        """
        Handles GET requests. The token is passed as a URL parameter.
        """
        email_verifier = EmailVerification()

        # try:
        # Decode the token and get the email
        payload = email_verifier.decode_token(token)
        print(payload)

        if payload:
            email = payload["email"]
            print(email)
            # Activate the user
            if email_verifier.activate_user(email):
                messages.info(
                    request, "Email verification successful and user activated."
                )
                if request.user.role == "Vendor":
                    return redirect("store:create-store")
                else:
                    return redirect("login")
            else:
                messages.info(request,
                    "Email verification failed. Invalid token or user does not exist.")
                return redirect("account-verification")
        else:
            messages.info(
                request,
                "Email verification failed. Invalid token or user does not exist.",
            )
            return redirect("account-verification")
        # except Exception as e:
        #     return HttpResponse(f"Error verifying email: {e}")


# accounts/views.py


class ResendVerificationEmailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        verified = VerificationCount.objects.get(user=request.user).is_verified
        print("verified", verified)
        if request.user.is_authenticated and not verified:
            add_count = VerificationCount.objects.get(user=request.user)
            add_count.count += 1
            add_count.save()
            EmailVerification().resend_verification(user=request.user)
            messages.success(
                request, "Verification email has been resent. Please check your inbox."
            )
            return redirect("account-verification")
        else:
            messages.error(
                request, "User is either not authenticated or already verified."
            )
        return redirect("account-verification")


@login_required
@user_passes_test(is_vendor, login_url=reverse_lazy("vendor_login"))
def account_verification(request):
    return render(request, "accounts/account_verification.html")


# class Login(LoginView):
#     template_name= "accounts/user-login.html"

#     def get(self, request):
#         form = LoginForm()
#         context = {
#             "form": form,
#         }
#         return render(request, self.template_name, context)

#     def post(self, request):

#         form = LoginForm(request.POST)

#         if form.is_valid():
#             # # Handle user authentication
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             print(user, username, password)
#             # user = form.get_user()
#             if user is not None:
#                 login(request, user)
#                 return redirect('store:store')  # Redirect to a success page
#             else:
#                 # Authentication failed, show an error message
#                 form.add_error(None, 'Invalid login credentials')
#                 return render(request, self.template_name, {"form": form})
#         else:
#             messages.error(request, f"Invalid login credentials")
#             return render(request, self.template_name, {"form": form})


class Login(LoginView):
    template_name = "accounts/user-login.html"
    redirect_authenticated_user = True  # Redirect if user is already logged in
    success_url = reverse_lazy("store:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.role == "Vendor":
            business_name = self.request.user.vendor.business_name
            logout(self.request)
            messages.error(
                self.request, "Vendors log in Not Allowed. Use store Login instead"
            )
            return redirect("vendor_login", business_name=business_name)
        return response


#     def get_success_url(self):
#         user = self.request.user
#         user_role = user.role  # Assuming you've stored the role in the user model

#         # Redirect the user based on their role
#         if user_role == 'Admin':
#             return '/vendor/'
#         elif user_role == 'Vendor':
#             return '/vendor/'
#         else:
#             return '/'

#     def form_valid(self, form):
#         user = form.get_user()
#         login(self.request, user)
#         return redirect(self.get_success_url())
# # VENDOR ACCOUNTS VIEW
# VENDOR SIGNUP VIEW


def vendor_signup(request):
    if request.method == "POST":
        form = VendorSignupForm(request.POST)
        user_form = SignupForm

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["business_name"],
                email=form.cleaned_data["business_email"],
                password=form.cleaned_data["password1"],
                role="Vendor",
            )

            verification = VerificationCount.objects.create(
                user=user, email=user.email, count=1
            )
            vendor = VendorProfile.objects.create(
                user=user,
                email=user.email,
                business_name=form.cleaned_data["business_name"],
            )
            email_verification = EmailVerification()

            # Generate token and send verification email
            token = email_verification.generate_token(user.email)
            email_sent = email_verification.send_verification_email(user)
            # log(
            #     user=user,
            #     action="Created a User Account, Verification Email Sent",
            #     obj=user,
            #     # extra={"title": foo.title},
            #     dateof=datetime.datetime.now(),
            # )

            messages.info(
                request,
                f"Created Bussiness {user.username}, a verification email has been sent to activate account",
            )
            return redirect("vendor_login", business_name=vendor.business_name)
        else:
            messages.error(request, f"Error Creating Account, Rectify error and retry")
            return render(
                request,
                "accounts/user-signup.html",
                {"vendor_form": form, "form": user_form},
            )


def business_name_exists(business_name):
    return VendorProfile.objects.filter(business_name=business_name).exists()


def vendor_login(request, business_name):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        next_url = request.POST.get("next", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next_url:
                return redirect(next_url)
            else:
                return redirect("store:vendor-home", business_name=business_name)
        else:
            # Return an 'invalid login' error message.
            context = {
                "error": "Invalid username or password",
                "business_name": business_name,
            }
            return render(request, "accounts/vendor-login.html", context)
    else:
        if business_name_exists(business_name):
            context = {"business_name": business_name}
            return render(request, "accounts/vendor-login.html", context=context)
        else:
            raise Http404("Business name does not exist")


def update_password(request):
    if request.method == "POST":
        current_password = request.POST["current_password"]
        new_password = request.POST["new_password"]
        user = User.objects.get(username=request.user.username)

        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password updated successfully")
            if request.user.role == "Vendor":
                return redirect("update_password")
            return redirect("store:settings")
        else:
            messages.error(request, "Current password is incorrect")
            return redirect("update_password")
    else:
        if request.user.role == "Vendor":
            business_name = request.user.vendor.business_name
            return render(
                request,
                "accounts/vendor-update-password.html",
                {"business_name": business_name},
            )
        else:
            return render(request, "accounts/user-update-password.html")


# class VendorSignupView:
#     templatee_name = "account/vendor/signup.html"

#     def get(self, request):
#         return render(request, self.template_name)

#     def post(self, request):
#         username = request.POST.get("username")
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         password2 = request.POST.get("password2")

#         if password == password2:
#             if User.objects.filter(email=email).exists():
#                 messages.info(request, "Email Already Used")
#                 return redirect("signup")
#             elif User.objects.filter(username=username).exists():
#                 messages.info(request, "Username Already Used")
#                 return redirect("signup")
#             else:
#                 user = User.objects.create_user(
#                     username=username, email=email, password=password
#                 )
#                 user.save()
#                 mydict = {"username": username}

#                 html_template = "register_email.html"
#                 html_message = render_to_string(html_template, context=mydict)
#                 subject = "Welcome to Service-Verse"
#                 email_from = settings.EMAIL_HOST_USER
#                 recipient_list = [email]
#                 message = EmailMessage(
#                     subject, html_message, email_from, recipient_list
#                 )
#                 message.content_subtype = "html"
#                 message.send()
#                 messages.success(
#                     request, f"Account for {username} created successfully"
#                 )
#                 return redirect("login")
#         else:
#             messages.info(request, "Password not the Same")
#             return redirect("signup")
# @login_required
# def deactivate_account(request):
#     user = request.user
#     user.is_active = False
#     user.save()
#     messages.success(request, 'Your account has been deactivated.')
#     return redirect('login')  # or wherever you want to redirect after deactivation

# Acount reactivation
# def login_view(request):
#     # ... your existing login code ...

#     user = authenticate(username=username, password=password)
#     if user is not None:
#         if user.is_active:
#             login(request, user)
#             # Redirect to a success page.
#         else:
#             # Send reactivation email
#             mail_subject = 'Reactivate your account.'
#             message = render_to_string('accounts/reactivate_account_email.html', {
#                 'user': user,
#                 'domain': get_current_site(request).domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': account_activation_token.make_token(user),
#             })
#             send_mail(mail_subject, message, 'info@mywebsite.com', [user.email])
#             return HttpResponse('Please confirm your email address to reactivate your account')
#     else:
#         # Return an 'invalid login' error message.

# def reactivate_account(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = get_user_model().objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         # log the user in and redirect them to a success page
#     else:
#         return HttpResponse('Activation link is invalid!')


def logout_view(request):
    logout(request)
    return redirect("/")
