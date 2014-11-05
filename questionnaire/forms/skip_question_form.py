from django import forms
from django.core.exceptions import ValidationError
from questionnaire.models import SkipQuestion


class SkipQuestionRuleForm(forms.ModelForm):
    class Meta:
        model = SkipQuestion

    def _clean_root_question(self):
        root_question = self.cleaned_data.get('root_question', None)
        skip_question = self.cleaned_data.get('skip_question', None)
        subsection = self.cleaned_data.get('subsection', None)

        if skip_question and root_question and skip_question.is_ordered_after(root_question, subsection):
            raise ValidationError("Root question must be before skip question")

        if self._is_same_question(root_question, skip_question):
            raise ValidationError("Root question cannot be the same as skip question")

        if root_question and skip_question and not self.in_the_same_subsection(root_question, skip_question):
            raise ValidationError("Both questions should belong to the same subsection")

    def _clean_response(self):
        response = self.cleaned_data.get('response', None)
        root_question = self.cleaned_data.get('root_question', None)
        if root_question and not response in root_question.options.all():
            self._errors['response'] = ["The selected option is not a valid option for the root question"]

    def clean(self):
        self._clean_root_question()
        self._clean_response()
        return super(SkipQuestionRuleForm, self).clean()

    def _is_same_question(self, root_question, skip_question):
        return root_question and root_question == skip_question and skip_question

    def in_the_same_subsection(self, root_question, skip_question):
        subsection_ = self.cleaned_data.get('subsection', None)
        root_question_groups = root_question.question_group.filter(subsection=subsection_)
        skip_question_groups = skip_question.question_group.filter(subsection=subsection_)
        return subsection_ and root_question_groups.exists() and skip_question_groups.exists()
