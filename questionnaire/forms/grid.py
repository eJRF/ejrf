from django import forms
from questionnaire.models import Question

GRID_TYPES = (('display_all', 'Display All'),
              ('allow_multiples', 'Add More'),
              ('hybrid', 'Hybrid'))


class GridForm(forms.Form):
    type = forms.ChoiceField(choices=GRID_TYPES)
    primary_question = forms.ModelChoiceField(queryset=Question.objects.filter(is_primary=True, answer_type='MultiChoice'), empty_label=None)
    columns = forms.ModelMultipleChoiceField(queryset=Question.objects.exclude(is_primary=True),
                                            widget=forms.SelectMultiple(attrs={'class': 'hide'}))

    def __init__(self, *args, **kwargs):
        self.subsection = kwargs.pop('subsection', None)
        super(GridForm, self).__init__(*args, **kwargs)

    def save(self):
        primary_question = self.cleaned_data.get('primary_question')
        non_primary_questions = self.cleaned_data.get('columns')
        grid_group = self._create_grid(primary_question, non_primary_questions)
        self._create_orders(primary_question, non_primary_questions, grid_group)
        return grid_group

    def _create_grid(self, primary_question, non_primary_questions):
        order = self.subsection.next_group_order() if self.subsection else 0
        grid_group = primary_question.question_group.create(subsection=self.subsection, grid=True, display_all=True, order=order)
        grid_group.question.add(*non_primary_questions)
        return grid_group

    def _create_orders(self, primary_question, non_primary_questions, grid_group):
        grid_group.orders.create(order=0, question=primary_question)
        for index, question in enumerate(non_primary_questions):
            grid_group.orders.create(order=index+1, question=question)