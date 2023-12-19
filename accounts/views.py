import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from accounts.models import User, VerificationCount
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.views import LoginView
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from store import settings
from accounts.forms import SignupForm, LoginForm
from pinax.eventlog.models import log
from accounts.emailverification import EmailVerification

# log(
#         user=request.user,
#         action="CREATED_FOO_WIDGET",
#         obj=foo,
#         extra={"title": foo.title},
#     )
# Create your views here.


# USer SIGN UP View
class UserSignup(View):
    template_name = "accounts/user-signup.html"
    # form = UserCreationForm()

    def get(self, request):
        form = SignupForm()
        context = {
            "form": form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = SignupForm(request.POST)
        print(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                verification = VerificationCount.objects.create(
                    user=user, email=user.email, count=1
                )

                email_verification = EmailVerification()

                # Generate token and send verification email
                token = email_verification.generate_token(user.email)
                email_sent = email_verification.send_email(user, token)
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
                return render(request, self.template_name, {"form": form})
        else:
            messages.error(request, f"Error Creating Account, Rectify error and retry")
            return render(request, self.template_name, {"form": form})


class VerifyEmailView(View):
    """
    View to handle email verification.
    """

    def get(self, request, token):
        """
        Handles GET requests. The token is passed as a URL parameter.
        """
        email_verifier = EmailVerification()

        try:
            # Decode the token and get the email
            payload = email_verifier.decode_token(token)
            email = payload["email"]

            # Activate the user
            if email_verifier.activate_user(email):
                return HttpResponse("Email verification successful and user activated.")
            else:
                return HttpResponse(
                    "Email verification failed. Invalid token or user does not exist."
                )
        except Exception as e:
            return HttpResponse(f"Error verifying email: {e}")


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


class VendorSignupView:
    templatee_name = "account/vendor/signup.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Used")
                return redirect("signup")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Already Used")
                return redirect("signup")
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password
                )
                user.save()
                mydict = {"username": username}

                html_template = "register_email.html"
                html_message = render_to_string(html_template, context=mydict)
                subject = "Welcome to Service-Verse"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                message = EmailMessage(
                    subject, html_message, email_from, recipient_list
                )
                message.content_subtype = "html"
                message.send()
                messages.success(
                    request, f"Account for {username} created successfully"
                )
                return redirect("login")
        else:
            messages.info(request, "Password not the Same")
            return redirect("signup")


def logout_view(request):
    logout(request)
    return redirect("/")
