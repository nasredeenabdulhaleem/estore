# from django import forms
# from django.contrib.auth.models import User

# class SignupForm(forms.Form):
#     username = forms.CharField(max_length=150)
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)
#     password2 = forms.CharField(widget=forms.PasswordInput)

#     def clean_username(self):
#         username = self.cleaned_data['username']
#         if User.objects.filter(username=username).exists():
#             raise forms.ValidationError("Username is already taken.")
#         return username

#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError("Email is already registered.")
#         return email


from django import forms

# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


class SignupForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Username"})
    )
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class VendorSignupForm(forms.Form):
    business_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Business Name"})
    )
    business_email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Business Email"})
    )
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
    )


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    next = forms.CharField(label="", widget=forms.HiddenInput(attrs={"value": "/"}))


# class VendorSignupForm(UserCreationForm):
#     email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
#     username = forms.CharField(
#         widget=forms.TextInput(attrs={"placeholder": "Username"})
#     )
#     password1 = forms.CharField(
#         label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Password"})
#     )
#     password2 = forms.CharField(
#         label="Confirm Password",
#         widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
#     )

#     class Meta:
#         model = User
#         fields = ["username", "email", "password1", "password2"]

