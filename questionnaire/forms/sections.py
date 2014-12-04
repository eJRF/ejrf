from django.forms import ModelForm
from django import forms

from questionnaire.models import Section, SubSection
from questionnaire.services.question_re_indexer import OrderBasedReIndexer
from questionnaire.utils.form_utils import _set_is_core


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
        questionnaire = self.initial['questionnaire']
        section_orders = list(
            Section.objects.filter(questionnaire=questionnaire).order_by('order').values_list('order', flat=True))
        if not section_orders:
            section_orders.append(1)
        elif not self.instance.id:
            section_orders.append(max(section_orders) + 1)
        unique_orders = set(section_orders)
        return zip(unique_orders, unique_orders)

    def _clean_is_core(self):
        user = self.initial.get('user')
        if user and self.instance.id and not user.user_profile.can_delete(self.instance):
            self.errors['name'] = 'You are not permitted to edit this section'

    def clean(self):
        self._clean_is_core()
        return super(SectionForm, self).clean()

    def save(self, commit=True, *args, **kwargs):
        section = super(SectionForm, self).save(commit=False)
        region = self.initial.get('region', None)
        section = _set_is_core(self.initial, section)
        if commit:
            based_re_indexer = OrderBasedReIndexer(section, self.cleaned_data['order'],
                                                   questionnaire=section.questionnaire, region=region)
            based_re_indexer.reorder()
        return section


class SubSectionForm(ModelForm):
    def save(self, commit=True, *args, **kwargs):
        subsection = super(SubSectionForm, self).save(commit=False, *args, **kwargs)
        if not self.instance.order:
            subsection.order = SubSection.get_next_order(self.instance.section.id)
            subsection = _set_is_core(self.initial, subsection)
        if commit:
            subsection.save()
        return subsection

    class Meta:
        model = SubSection
        fields = ['title', 'description']
        widgets = {'description': forms.Textarea(attrs={"rows": 4, "cols": 50})}