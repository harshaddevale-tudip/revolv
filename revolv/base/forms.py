from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from django.utils.text import capfirst


class SignupForm(UserCreationForm):
    """
    Form for a user to sign up for an account. Note that we manually clean
    and save the first and last name of the user and their email, since
    django.contrib.auth.forms.UserCreationForm does not do that by default.
    """
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last name")
    subscribed_to_newsletter = forms.BooleanField(initial=True, required=False, label="Subscribe me to the RE-volv Newsletter.", help_text="Subscribe me to the RE-volv Newsletter")


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
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            user.revolvuserprofile.subscribed_to_newsletter = self.cleaned_data["subscribed_to_newsletter"]
            user.revolvuserprofile.save()
        return user

    def ensure_authenticated_user(self):
        """
        Return the User model related to this valid form, or raise an
        IntegrityError if it does not exist (because it should).
        """
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password2')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            return user
        raise IntegrityError(
            "User model could not be saved during signup process."
        )

class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.CharField(max_length=254)
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
        username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'placeholder': 'Search'}))
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)

        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst('Username or Email')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
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