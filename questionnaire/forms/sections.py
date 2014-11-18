from django.forms import ModelForm
from django import forms

from questionnaire.models import Section, SubSection
from questionnaire.services.question_re_indexer import OrderBasedReIndexer


class SectionForm(ModelForm):
    order = forms.ChoiceField(choices=())

    def __init__(self, *args, **kwargs):
        super(SectionForm, self).__init__(*args, **kwargs)
        self.fields['order'].choices = self._get_options()
        self.fields['order'].label = 'Position'
    class Meta:
        model = Section
        fields = ['questionnaire', 'name', 'title', 'description', 'order']
        widgets = {'questionnaire': forms.HiddenInput(),
                   'description': forms.Textarea(attrs={"rows": 4, "cols": 40})}

    def _get_options(self):
        section_orders = Section.objects.order_by('order').values_list('order', flat=True)
        if self.instance.id:
            questionnaire = self.instance.questionnaire
            orders = list(section_orders.filter(questionnaire=questionnaire))
            unique_orders = set(orders)
            return zip(unique_orders, unique_orders)

        max_plus_one = max(section_orders) + 1
        all_orders = list(section_orders)
        all_orders.append(max_plus_one)
        unique_orders = set(all_orders)
        return zip(unique_orders, unique_orders)

    def save(self, commit=True):
        section = super(SectionForm, self).save(commit)
        if commit and not section.is_last_in(section.questionnaire):
            based_re_indexer = OrderBasedReIndexer(section, self.cleaned_data['order'],
                                                   questionnaire=section.questionnaire)
            based_re_indexer.reorder()
        return section


class SubSectionForm(ModelForm):
    def save(self, commit=True, *args, **kwargs):
        subsection = super(SubSectionForm, self).save(commit=False, *args, **kwargs)
        if not self.instance.order:
            subsection.order = SubSection.get_next_order(self.instance.section.id)
        if commit:
            subsection.save()
        return subsection

    class Meta:
        model = SubSection
        fields = ['title', 'description']
        widgets = {'description': forms.Textarea(attrs={"rows": 4, "cols": 50})}