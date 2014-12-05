from django.forms import ModelForm
from django import forms
from django.forms.models import model_to_dict

from questionnaire.models import Question, QuestionOption, Questionnaire
from questionnaire.utils.answer_type import AnswerTypes


class QuestionForm(ModelForm):
    KNOWN_OPTIONS = ["Yes, No",
                     "Yes, No, NR",
                     "Yes, No, NR, ND",
                     "Male, Female, Both",
                     "Local currency, US $",
                     "National, Sub national",
    ]

    options = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, region=None, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.region = region
        self.fields['answer_type'].choices = self._set_answer_type_choices()
        self.fields['answer_type'].label = 'Response Type'
        self.fields['text'].label = 'Display label (Online)'
        self.fields['export_label'].label = 'Export label (Detail)'
        self.fields['theme'].empty_label = 'Select theme'
        self.fields['answer_sub_type'].label = 'Response sub type'
        self.fields['answer_sub_type'].attrs = "data-ng-show='allOptions'"
        self.fields['answer_sub_type'].choices = self._set_subtype_choices()

    class Meta:
        ANGULAR_OPTIONS_AND_FILTER = "option.text for option in allOptions track by option.value"
        model = Question
        fields = (
            'text', 'export_label', 'instructions', 'answer_type', 'answer_sub_type', 'options', 'theme', 'is_primary')
        widgets = {'text': forms.Textarea(attrs={"rows": 6, "cols": 50}),
                   'instructions': forms.Textarea(attrs={"rows": 25, "cols": 50}),
                   'answer_type': forms.Select(attrs={"data-ng-model": "answerType"}),
                   'answer_sub_type': forms.Select(attrs={"data-ng-model": "answerSubType",
                                                          "data-ng-options": ANGULAR_OPTIONS_AND_FILTER}),
                   'theme': forms.Select(),
                   'export_label': forms.Textarea(attrs={"rows": 2, "cols": 50})}

    def _set_subtype_choices(self):
        choices = self.fields['answer_sub_type'].choices
        choices[0] = ('', 'Select a Sub-Type', )
        return choices

    def clean(self):
        self._clean_options()
        self._clean_export_label()
        self._clean_answer_sub_type()
        return super(QuestionForm, self).clean()

    def _clean_options(self):
        answer_type = self.cleaned_data.get('answer_type', None)
        options = dict(self.data).get('options', [])
        options = filter(None, options)
        if (answer_type and AnswerTypes.is_mutlichoice_or_multiple(answer_type)) and len(options) < 1:
            message = "%s questions must have at least one option" % answer_type
            self._errors['answer_type'] = self.error_class([message])
            del self.cleaned_data['answer_type']
        return options

    def _clean_answer_sub_type(self):
        answer_type = self.cleaned_data.get('answer_type', None)
        answer_sub_type = self.cleaned_data.get('answer_sub_type', None)
        if answer_type and AnswerTypes.has_subtype(answer_type) and not AnswerTypes.is_valid_sub_type(answer_type,
                                                                                                      answer_sub_type):
            message = "This field is required if you select '%s'" % answer_type
            self._errors['answer_sub_type'] = self.error_class([message])
            del self.cleaned_data['answer_sub_type']

    def _clean_export_label(self):
        export_label = self.cleaned_data.get('export_label', None)
        if not export_label:
            message = "All questions must have export label."
            self._errors['export_label'] = self.error_class([message])
            del self.cleaned_data['export_label']
        return export_label

    def save(self, commit=True):
        if self._editing_published_question():
            question = self._duplicate_question()
            self._reassign_to_unpublished_questionnaires(question)
            self._save_options_if_multichoice(question)
            return question
        return self._save(commit)

    def _reassign_to_unpublished_questionnaires(self, question):
        unpublished_in_questionnaire = self.instance.questionnaires().exclude(status=Questionnaire.PUBLISHED)
        for questionnaire in unpublished_in_questionnaire:
            for group in self.instance.question_groups_in(questionnaire):
                group.question.remove(self.instance)
                group.question.add(question)
                self._assign_order(question, group)

    def _assign_order(self, question, group):
        parent_group = group.parent or group
        order = self.instance.orders.get(question_group=parent_group)
        question_order = order.order
        order.delete()
        question.orders.create(question_group=parent_group, order=question_order)

    def _duplicate_question(self):
        attributes = model_to_dict(self.instance, exclude=('id',))
        attributes.update({'parent': self.instance})
        del attributes['region']
        del attributes['theme']
        return Question.objects.create(region=self.instance.region, theme=self.instance.theme, **attributes)

    def _editing_published_question(self):
        if not (self.instance and self.instance.id):
            return False
        published_in_questionnaire = self.instance.questionnaires().filter(status=Questionnaire.PUBLISHED)
        if published_in_questionnaire.exists():
            return True
        return False

    def _save(self, commit=True):
        question = super(QuestionForm, self).save(commit=False)
        question.UID = Question.next_uid()
        if self.region:
            question.region = self.region
        if commit:
            question.save()
            self._save_options_if_multichoice(question)
        return question

    def _save_options_if_multichoice(self, question):
        options = dict(self.data).get('options', [])
        options = filter(lambda text: text.strip(), options)
        if options and AnswerTypes.is_mutlichoice_or_multiple(question.answer_type):
            for grouped_option in options:
                for option in grouped_option.split(','):
                    QuestionOption.objects.get_or_create(text=option.strip(), question=question)

    def _set_answer_type_choices(self):
        choices = self.fields['answer_type'].choices
        choices[0] = ('', 'Response type', )
        return choices
