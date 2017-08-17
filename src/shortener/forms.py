from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import URLValidator


User = get_user_model()


class SubmitUrlForm(forms.Form):
    """
    Form used to submit URL to shorten.
    """
    url = forms.CharField(
        max_length=254,
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Paste a link to shorten it',
                'class': 'form-control'
            }
        )
    )

    def clean_url(self):
        """
        Validates URLs that ones without protocol can also pass.
        """
        url = self.cleaned_data['url']
        validator = URLValidator()
        try:
            validator(url)
        except forms.ValidationError:
            url = 'http://{}'.format(url)
            try:
                validator(url)
            except forms.ValidationError:
                raise forms.ValidationError('Invalid URL', code='invalid')
        return url


class RegistrationForm(UserCreationForm):
    """
    Form for registering a new user account.
    """
    email = forms.EmailField(
        help_text='email address',
        required=True
    )

    class Meta(UserCreationForm.Meta):
        fields = [
            User.USERNAME_FIELD,
            'email',
            'password1',
            'password2'
        ]
