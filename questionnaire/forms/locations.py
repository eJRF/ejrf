from django.forms import ModelForm

from questionnaire.models import Region


class RegionForm(ModelForm):
    class Meta:
        model = Region
