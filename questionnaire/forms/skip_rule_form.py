from django import forms
from django.core.exceptions import ValidationError

from questionnaire.models import SkipRule
from questionnaire.models.skip_rule import SkipQuestion, SkipSubsection


class SkipRuleForm(forms.ModelForm):
    class Meta:
        model = SkipRule

    def _clean_response(self):
        response = self.cleaned_data.get('response', None)
        root_question = self.cleaned_data.get('root_question', None)
        if root_question and not response in root_question.options.all():
            self._errors['response'] = ["The selected option is not a valid option for the root question"]

    def clean(self):
        self._clean_response()
        return super(SkipRuleForm, self).clean()

    def in_the_same_subsection(self, root_question, skip_question):
        subsection_ = self.cleaned_data.get('subsection', None)
        root_question_groups = root_question.question_group.filter(subsection=subsection_)
        skip_question_groups = skip_question.question_group.filter(subsection=subsection_)
        return subsection_ and root_question_groups.exists() and skip_question_groups.exists()


class SkipQuestionForm(SkipRuleForm):
    class Meta:
        model = SkipQuestion

    def clean(self):
        self._clean_root_question()
        self._clean_is_unique()
        return super(SkipQuestionForm, self).clean()

    def _clean_is_unique(self):
        root_question = self.cleaned_data.get('root_question', None)
        skip_question = self.cleaned_data.get('skip_question', None)
        subsection = self.cleaned_data.get('subsection', None)
        response = self.cleaned_data.get('response', None)
        rules = SkipQuestion.objects.filter(root_question=root_question, skip_question=skip_question,
                                            subsection=subsection, response=response)
        if rules.exists():
            self._errors['root_question'] = ["This rule already exists"]

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

    def _is_same_question(self, root_question, skip_question):
        return root_question and root_question == skip_question and skip_question


class SkipSubsectionForm(SkipRuleForm):
    class Meta:
        model = SkipSubsection

    def clean(self):
        self._clean_is_unique()
        self._clean_root_question()
        self._clean_subsection()
        return super(SkipSubsectionForm, self).clean()

    def _clean_subsection(self):
        skip_subsection = self.cleaned_data.get('skip_subsection', None)
        subsection = self.cleaned_data.get('subsection', None)
        if skip_subsection and subsection and skip_subsection.order < subsection.order:
            self.errors['skip_subsection'] = [
                'The subsection you have specified to skip comes before the root question.']

    def _clean_is_unique(self):
        root_question = self.cleaned_data.get('root_question', None)
        skip_subsection = self.cleaned_data.get('skip_subsection', None)
        subsection = self.cleaned_data.get('subsection', None)
        response = self.cleaned_data.get('response', None)
        rules = SkipSubsection.objects.filter(root_question=root_question, skip_subsection=skip_subsection,
                                              subsection=subsection, response=response)
        if rules.exists():
            self._errors['root_question'] = ["This rule already exists"]

    def _clean_root_question(self):
        skip_subsection = self.cleaned_data.get('skip_subsection', None)
        subsection = self.cleaned_data.get('subsection', None)
        if skip_subsection == subsection:
            self.errors['skip_subsection'] = ['You cannot skip the subsection which the root question is in.']