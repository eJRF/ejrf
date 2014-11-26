from django.forms import Form
from django import forms

from questionnaire.models import Question, QuestionGroup


class AssignQuestionForm(Form):
    questions = forms.ModelMultipleChoiceField(queryset=None, label='')

    def __init__(self, *args, **kwargs):
        self.subsection = kwargs.pop('subsection', None)
        self.region = kwargs.pop('region', None)
        super(AssignQuestionForm, self).__init__(*args, **kwargs)
        self.fields['questions'].queryset = self._get_questions_query_set()

    def _get_questions_query_set(self):
        return Question.objects.filter(region=self.region)

    def save(self, commit=True, *args, **kwargs):
        question_group = self._get_question_group()
        args = list(self.cleaned_data['questions'])
        question_group.question.add(*args)
        self._create_group_orders(question_group)

    def _create_group_orders(self, question_group):
        max_order = question_group.max_questions_order()
        for index, question in enumerate(self.cleaned_data['questions']):
            question.orders.create(question_group=question_group, order=max_order + index + 1)

    def _get_question_group(self):
        if self.subsection.question_group.exists():
            question_group = self.subsection.question_group.filter(parent__isnull=True).order_by('-order')[0]
            if question_group.grid:
                return self.subsection.question_group.create(order=question_group.order + 1)
            return question_group
        next_order = QuestionGroup.next_order_in(self.subsection)
        return self.subsection.question_group.create(order=next_order)
