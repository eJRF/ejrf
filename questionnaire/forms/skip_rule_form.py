from django import forms
from django.core.exceptions import ValidationError

from questionnaire.models import SkipRule


class SkipRuleForm(forms.ModelForm):
    class Meta:
        model = SkipRule

    def _clean_root_question(self):
        root_question = self.cleaned_data.get('root_question', None)
        skip_question = self.cleaned_data.get('skip_question', None)
        subsection = self.cleaned_data.get('subsection', None)

        if self._is_same_question(root_question, skip_question):
            raise ValidationError("Root question cannot be the same as skip question")

        if root_question and skip_question and not self.in_the_same_subsection(root_question, skip_question):
            raise ValidationError("Both questions should belong to the same subsection")

        if skip_question and root_question and not skip_question.is_ordered_after(root_question, subsection):
            self._errors['root_question'] = ["Root question must be before skip question"]


    def _clean_response(self):
        response = self.cleaned_data.get('response', None)
        root_question = self.cleaned_data.get('root_question', None)
        if root_question and not response in root_question.options.all():
            self._errors['response'] = ["The selected option is not a valid option for the root question"]

    def _clean_item_to_skip(self):
        subsection = self.cleaned_data.get('skip_subsection', None)
        question = self.cleaned_data.get('skip_question', None)
        if subsection is None and question is None:
            self._errors['skip_question'] = ["This field is required."]
            self._errors['skip_subsection'] = ["This field is required."]


    def clean(self):
        if len(self._errors) == 0:
            self._clean_item_to_skip()
        self._clean_root_question()
        self._clean_response()
        return super(SkipRuleForm, self).clean()

    def _is_same_question(self, root_question, skip_question):
        return root_question and root_question == skip_question and skip_question

    def in_the_same_subsection(self, root_question, skip_question):
        subsection_ = self.cleaned_data.get('subsection', None)
        root_question_groups = root_question.question_group.filter(subsection=subsection_)
        skip_question_groups = skip_question.question_group.filter(subsection=subsection_)
        return subsection_ and root_question_groups.exists() and skip_question_groups.exists()