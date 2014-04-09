import copy
from django import forms
from django.forms.util import ErrorDict
from django.forms import ModelForm, ModelChoiceField
from questionnaire.forms.custom_widgets import MultiChoiceAnswerSelectWidget

from questionnaire.models import NumericalAnswer, TextAnswer, DateAnswer, MultiChoiceAnswer, QuestionOption


class AnswerForm(ModelForm):
    def __init__(self,  *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.question = self._get_question(kwargs)
        self.fields['response'].required = self.question.is_required
        self._initial = self._set_initial(kwargs)
        self.is_editing = False
        self._set_instance()
        self.question_group = self._initial['group'] if self._initial else None

    def _set_initial(self, kwargs):
        initial = kwargs['initial'] if 'initial' in kwargs else {}
        if self.data and 'response' and self.data.keys():
            if 'response' in initial.keys():
                del initial['response']
        return initial

    def _set_instance(self):
        if 'answer' in self._initial:
            self.is_editing = True
            self.instance = self._initial['answer']

    def show_is_required_errors(self):
        if self.question.is_required and not self.data and not self._initial.get('response', None):
            self._errors = self._errors or ErrorDict()
            self._errors['response'] = self.error_class(['This field is required.'])

    def save(self, commit=True, *args, **kwargs):
        if self.is_editing:
            return super(AnswerForm, self).save(commit=commit, *args, **kwargs)
        return self._create_new_answer(*args, **kwargs)

    def _create_new_answer(self, *args, **kwargs):
        answer = super(AnswerForm, self).save(commit=False, *args, **kwargs)
        self._add_extra_attributes_to(answer)
        answer.save()
        return answer

    def _add_extra_attributes_to(self, answer):
        for attribute in self._initial.keys():
            setattr(answer, attribute, self._initial[attribute])

    def _get_question(self, kwargs):
        return kwargs['initial'].get('question', None)


class NumericalAnswerForm(AnswerForm):
    class Meta:
        model = NumericalAnswer
        exclude = ('question', 'status', 'country', 'version', 'code', 'questionnaire')


class TextAnswerForm(AnswerForm):
    response = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = TextAnswer
        exclude = ('question', 'status', 'country', 'version', 'code', 'questionnaire')


class DateAnswerForm(AnswerForm):
    class Meta:
        model = DateAnswer
        exclude = ('question', 'status', 'country', 'version', 'code', 'questionnaire')
        widgets = {
            'response': forms.DateInput(attrs={'class': 'form-control datetimepicker', 'data-format':'YYYY-MM-DD'})
        }


class MultiChoiceAnswerForm(AnswerForm):
    response = ModelChoiceField(queryset=None, widget=forms.Select(), required=False)
    specified_option = forms.CharField(max_length=50, widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(MultiChoiceAnswerForm, self).__init__(*args, **kwargs)
        query_set = self._get_response_choices(kwargs)
        self.fields['response'].widget = self._get_response_widget(query_set)
        self.fields['response'].queryset = query_set
        self.fields['response'].empty_label = self._set_response_label(query_set)
        self.options = query_set
        self._set_data()

    def _set_data(self):
        if self.data:
            new_data = copy.deepcopy(self.data)
            self.data = new_data

    def _set_response_label(self, query_set):
        if self.widget_is_radio_button(query_set) or query_set.count() == 1:
            return None
        return "Choose One"

    def widget_is_radio_button(self, query_set):
        group = self._initial['group']
        if group.grid and not group.hybrid:
            return False
        return query_set.count() == 2 or query_set.filter(text='Yes').exists() or query_set.filter(text='Male').exists()

    def _get_response_widget(self, query_set):
        if self.widget_is_radio_button(query_set):
            return forms.RadioSelect()
        if query_set.exclude(instructions=None).exists():
            return MultiChoiceAnswerSelectWidget(question_options=query_set)
        return forms.Select()

    def _get_response_choices(self, kwargs):
        all_options = self.question.options.all()
        if 'option' in self._initial:
            return all_options.filter(id=self._initial.get('option').id).order_by('text')
        return all_options.order_by('text')

    def save(self, commit=True, *args, **kwargs):
        answer = super(MultiChoiceAnswerForm, self).save(commit=False, *args, **kwargs)
        self._save_specified_option_to(answer)
        if commit:
            answer.save()
        return answer

    def _save_specified_option_to(self, answer):
        specified_option = self.cleaned_data.get('specified_option', None)
        if specified_option:
            UID = QuestionOption.generate_uid()
            new_option, _ = self.question.options.get_or_create(text=specified_option, UID=UID)
            answer.response = new_option
            self.data[self.add_prefix('response')] = new_option.id

    class Meta:
        model = MultiChoiceAnswer
        exclude = ('question', 'status', 'country', 'version', 'code', 'questionnaire')