from django import forms
from django.core.validators import URLValidator


class SubmitUrlForm(forms.Form):
    """
    Form used to submit URL to shorten.
    """
    url = forms.CharField(max_length=254, label='Submit URL')

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
