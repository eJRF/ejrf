from django import forms
from questionnaire.models import Question

GRID_TYPES = (('display_all', 'Display All'),
              ('allow_multiples', 'Add More'),
              ('hybrid', 'Hybrid'))


class GridForm(forms.Form):
    type = forms.ChoiceField(choices=GRID_TYPES)
    primary_question = forms.ModelChoiceField(queryset=Question.objects.filter(is_primary=True), empty_label=None)
    column = forms.ModelMultipleChoiceField(queryset=Question.objects.exclude(is_primary=True))

