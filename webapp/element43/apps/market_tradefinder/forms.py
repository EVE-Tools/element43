"""
Forms for the tradefinder.
"""

from django import forms

# Models
from eve_db.models import MapRegion


# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary. If/when Django ticket #3515
# lands in trunk, this will no longer be necessary.
attrs_dict = {'class': 'required form-control'}


class TradefinderForm(forms.Form):
    """
    Tradefinder form.
    """

    start = forms.CharField(initial="The Forge")
    destination = forms.CharField(initial="The Forge")

    def clean_start(self):
        """
        Validate the start region.
        """
        existing = MapRegion.objects.filter(name__iexact=self.cleaned_data['start'])

        if existing.exists():
            return existing[0]
        else:
            raise forms.ValidationError("We could not find that region.")

    def clean_destination(self):
        """
        Validate the destination region.
        """
        existing = MapRegion.objects.filter(name__iexact=self.cleaned_data['destination'])

        if existing.exists():
            return existing[0]
        else:
            raise forms.ValidationError("We could not find that region.")

    def clean(self):
        return self.cleaned_data
