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

    def _set_is_core(self, section):
        user = self.initial.get('user')
        if section.id:
            return section
        elif user and user.user_profile.region:
            section.is_core = False
        else:
            section.is_core = True
        return section

    def save(self, commit=True, *args, **kwargs):
        section = super(SectionForm, self).save(commit=False)
        region = self.initial.get('region', None)
        section = self._set_is_core(section)
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
        if commit:
            subsection.save()
        return subsection

    class Meta:
        model = SubSection
        fields = ['title', 'description']
        widgets = {'description': forms.Textarea(attrs={"rows": 4, "cols": 50})}