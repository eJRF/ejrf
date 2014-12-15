import copy
from django import forms
from django.forms.util import ErrorDict
from django.forms import ModelForm, ModelChoiceField, ModelMultipleChoiceField

from questionnaire.forms.custom_widgets import MultiChoiceAnswerSelectWidget, SkipRuleRadioWidget
from questionnaire.models import NumericalAnswer, TextAnswer, DateAnswer, MultiChoiceAnswer, QuestionOption
from questionnaire.models.answers import MultipleResponseAnswer
from questionnaire.utils.answer_type import AnswerTypes
from questionnaire.utils.model_utils import number_from


class AnswerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.question = self._get_question(kwargs)
        self.fields['response'].required = self.question.is_required
        self._initial = self._set_initial(kwargs)
        self.is_editing = False
        self._set_instance()
        self.question_group = self._initial['group'] if self._initial else None
        self.fields['response'].widget.attrs.update({'class': 'input-question-id-%s' % self.question.id})


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
    ZERO = '0'
    NR = 'NR'
    ND = 'ND'

    class Meta:
        model = NumericalAnswer
        exclude = ('question', 'status', 'country', 'version', 'code', 'questionnaire', 'old_response')

    def clean(self):
        self._clean_response()
        return super(NumericalAnswerForm, self).clean()

    def _clean_response(self):
        response = self.cleaned_data.get('response', '').strip()
        a_valid_number = number_from(response)
        if response and not (response == self.ZERO or response == self.NR or response == self.ND or a_valid_number):
            self._errors['response'] = 'Enter a number or Either NR or ND if this question is irrelevant'
        elif a_valid_number and self._matches_answer_sub_type(a_valid_number):
            self._errors['response'] = "Response should be a whole number."

    def _matches_answer_sub_type(self, num):
        return AnswerTypes.is_integer(self.question.answer_sub_type) and not float(num).is_integer()


class TextAnswerForm(AnswerForm):
    response = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = TextAnswer
        exclude = ('question', 'status', 'country', 'version', 'code', 'questionnaire')


class DateAnswerForm(AnswerForm):
    def __init__(self, *args, **kwargs):
        super(DateAnswerForm, self).__init__(*args, **kwargs)
        self.fields['response'].widget = self._get_date_widget(self._initial['question'].answer_sub_type)

    class Meta:
        model = DateAnswer
        exclude = ('question', 'status', 'country', 'version', 'code', 'questionnaire', 'old_response')

    def _get_date_widget(self, date_answer_sub_type):
        if date_answer_sub_type == "MM/YYYY":
            return forms.DateInput(attrs={'class': 'form-control date-time-picker', 'data-date-format': 'mm/yyyy',
                                          'data-date-option': 'mm'})
        else:
            return forms.DateInput(attrs={'class': 'form-control date-time-picker input-question-id-%s' % self.question.id, 'data-date-format': 'dd/mm/yyyy',
                                          'data-date-option': 'dd'})

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
        if 'option' in self.initial.keys() and self.initial['question'].is_primary:
            return forms.Select(attrs={'class': 'hide'})
        if self.widget_is_radio_button(query_set):
            return SkipRuleRadioWidget(self.question_group.subsection, attrs={'class': 'input-question-id-%s' % self.question.id})
        if query_set.exclude(instructions=None).exists() or query_set.exclude(skip_rules=None).exists():
            return MultiChoiceAnswerSelectWidget(self.question_group.subsection, question_options=query_set, attrs={'class': 'input-question-id-%s' % self.question.id})
        return forms.Select(attrs={'class': 'input-question-id-%s' % self.question.id})

    def _get_response_choices(self, kwargs):
        all_options = self.question.options.order_by('order')
        if 'option' in self._initial:
            return all_options.filter(id=self._initial.get('option').id).order_by('order')
        return all_options.order_by('order')

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


class MultipleResponseForm(AnswerForm):
    response = ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple(), required=False, )

    def __init__(self, *args, **kwargs):
        super(MultipleResponseForm, self).__init__(*args, **kwargs)
        options_all = self.question.options.all()
        self.fields['response'].queryset = options_all
        self.options = options_all

    class Meta:
        model = MultipleResponseAnswer
        exclude = ('question', 'status', 'country', 'version', 'code', 'questionnaire')

    def _clean_response(self):
        response = self.cleaned_data.get('response', [])
        selected_options = [option in self.options for option in response]
        if len(response) != selected_options.count(True):
            message = 'Select a valid choice. The selected option is not one of the available choices.'
            self._errors['response'] = self.error_class([message])

    def clean(self):
        self._clean_response()
        return super(MultipleResponseForm, self).clean()

    def save(self, commit=True, *args, **kwargs):
        answer = super(MultipleResponseForm, self).save(commit=False, *args, **kwargs)
        answer.save()
        if commit:
            self.save_m2m()
        return answer