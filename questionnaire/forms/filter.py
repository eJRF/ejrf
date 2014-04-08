from django import forms
from django.contrib.auth.models import Group
from questionnaire.models import Region, Organization, Country, Theme, Questionnaire, Question


class UserFilterForm(forms.Form):
    organization = forms.ModelChoiceField(queryset=Organization.objects.order_by('name'),
                                          empty_label="All",
                                          widget=forms.Select(attrs={"class": 'form-control region-select'}),
                                          required=False)
    region = forms.ModelChoiceField(queryset=Region.objects.all(), empty_label="All",
                                    widget=forms.Select(attrs={"class": 'form-control region-select'}), required=False)

    role = forms.ModelChoiceField(queryset=Group.objects.order_by('name'), empty_label="All",
                                  widget=forms.Select(attrs={"class": 'form-control region-select'}), required=False)


class ExportFilterForm(forms.Form):
    regions = forms.ModelMultipleChoiceField(queryset=Region.objects.all(),
                                             widget=forms.CheckboxSelectMultiple(), required=False)
    countries = forms.ModelMultipleChoiceField(queryset=Country.objects.order_by('name'),
                                               widget=forms.CheckboxSelectMultiple(), required=False)
    themes = forms.ModelMultipleChoiceField(queryset=Theme.objects.order_by('name'),
                                            widget=forms.CheckboxSelectMultiple(), required=False)
    year = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), required=False, choices=[])

    def __init__(self, *args, **kwargs):
        super(ExportFilterForm, self).__init__(*args, **kwargs)
        self.fields['year'].choices = self._set_year_choices()

    @staticmethod
    def _set_year_choices():
        choices = []
        years_with_questionnaires = set(Questionnaire.objects.all().values_list('year', flat=True))
        choices.extend((year, year) for year in years_with_questionnaires)
        return choices


class QuestionFilterForm(forms.Form):
    theme = forms.ModelChoiceField(queryset=Theme.objects.all().order_by('name'),
                                   empty_label="All",
                                   widget=forms.Select(attrs={"class": 'form-control'}),required=False)
    answer_type = forms.ChoiceField(widget=forms.Select(attrs={"class": 'form-control'}), required=False,
                                    choices=Question.ANSWER_TYPES)

    def __init__(self, *args, **kwargs):
        super(QuestionFilterForm, self).__init__(*args, **kwargs)
        self.fields['answer_type'].choices = self.add_all_option()

    def add_all_option(self):
        choices = self.fields['answer_type'].choices
        choices.insert(0, ('', 'All'))
        return choices