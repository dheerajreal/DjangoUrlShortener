from django import forms

from .models import UrlRecord


class UrlForm(forms.ModelForm):
    original_url = forms.URLField(
        label="Original URL",
        help_text="The URL that you want to shorten"
    )

    class Meta:
        model = UrlRecord
        fields = ["original_url"]
