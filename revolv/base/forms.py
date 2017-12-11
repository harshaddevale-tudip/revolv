from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from django.utils.text import capfirst
from models import RevolvUserProfile

def generate_username(firstname, lastname):
    firstname = firstname
    lastname = lastname

    username = '%s%s' % (firstname[0], lastname)
    if User.objects.filter(username=username).count() > 0:
        username = '%s%s' % (firstname, lastname[0])
        if User.objects.filter(username=username).count() > 0:
            users = User.objects.filter(username__regex=r'^%s[1-9]{1,}$' % firstname).order_by('username').values(
                'username')
            if len(users) > 0:
                last_number_used = map(lambda x: int(x['username'].replace(firstname, '')), users)
                last_number_used.sort()
                last_number_used = last_number_used[-1]
                number = last_number_used + 1
                username = '%s%s' % (firstname, number)
            else:
                username = '%s%s' % (firstname, 1)

    return username

class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_username': ("A user with that username already exists."),
        'password_mismatch': ("The two password fields didn't match."),
    }

    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label=("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("email",)


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class SignupForm(UserCreationForm):
    """
    Form for a user to sign up for an account. Note that we manually clean
    and save the first and last name of the user and their email, since
    django.contrib.auth.forms.UserCreationForm does not do that by default.
    """
    # email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last name")
    subscribed_to_newsletter = forms.BooleanField(initial=True, required=False, label="Subscribe me to the RE-volv Newsletter.", help_text="Subscribe me to the RE-volv Newsletter")
    zipcode = forms.CharField(label="Zipcode", max_length=10)

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email already used")
        return data


    def save(self, commit=True):
        """
        On save of the form, update the associated user profile with first and
        last names.
        """
        user = super(SignupForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        # user.email = self.cleaned_data["email"]
        user.username = generate_username(user.first_name, user.last_name)
        if commit:
            user.save()
            user.revolvuserprofile.subscribed_to_newsletter = self.cleaned_data["subscribed_to_newsletter"]
            user.revolvuserprofile.zipcode = self.cleaned_data["zipcode"]
            user.revolvuserprofile.save()
        return user

    def ensure_authenticated_user(self):
        """
        Return the User model related to this valid form, or raise an
        IntegrityError if it does not exist (because it should).
        """
        email = self.cleaned_data['email']
        if email:
            try:
                user = User.objects.get(email__iexact=email)
                if user.check_password(self.cleaned_data['password2']):
                    return user
            except ObjectDoesNotExist:
                pass
        return None

class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    email = forms.CharField(max_length=254)
    password = forms.CharField(label=("Password"), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': ("Please enter a correct username and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': ("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        # Set the label for the "username" field.
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)

        if self.fields['email'].label is None:
            self.fields['email'].label = capfirst('Username or Email')

    def clean(self):
        username = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(email=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'email': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class RevolvUserProfileForm(forms.ModelForm):
    class Meta:
        model = RevolvUserProfile
        fields = ['subscribed_to_newsletter', 'subscribed_to_updates','subscribed_to_repayment_notifications']


class UpdateUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        unique_together = ["email"]

    email = forms.EmailField(label="Email")
    def clean_email(self):
        data = self.cleaned_data['email']
        username = self.cleaned_data['username']
        # user=User.objects.get(id=self.user_cache.id)
        if User.objects.filter(email=data).exclude(username=username).exists():
            raise forms.ValidationError("This email already used")
        return data
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last name")




