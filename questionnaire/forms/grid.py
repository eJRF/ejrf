from django import forms
from questionnaire.forms.custom_widgets import MultiChoiceQuestionSelectWidget
from questionnaire.models import Question

GRID_TYPES = (('', 'Choose One'),
              ('display_all', 'Display All'),
              ('allow_multiples', 'Add More'),
              ('hybrid', 'Hybrid'))


class GridForm(forms.Form):
    type = forms.ChoiceField(choices=GRID_TYPES)
    primary_question = forms.ModelChoiceField(queryset=Question.objects.filter(is_primary=True), empty_label='Choose One',
                                              widget=MultiChoiceQuestionSelectWidget())
    columns = forms.ModelMultipleChoiceField(queryset=Question.objects.exclude(is_primary=True),
                                            widget=forms.SelectMultiple(attrs={'class': 'hide'}))

    def __init__(self, *args, **kwargs):
        self.subsection = kwargs.pop('subsection', None)
        super(GridForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(GridForm, self).clean()
        type = cleaned_data.get('type')
        primary_question = cleaned_data.get('primary_question')
        if not type or not primary_question:
            return cleaned_data
        if not primary_question.is_multichoice() and (type == 'display_all' or type == 'hybrid'):
            message = 'This type of grid requires a multichoice primary question.'
            self._errors['primary_question'] = self.error_class([message])
            del self.cleaned_data['primary_question']
        return cleaned_data

    def save(self):
        primary_question = self.cleaned_data.get('primary_question')
        non_primary_questions = self.cleaned_data.get('columns')
        grid_group = self._create_grid(primary_question, non_primary_questions)
        self._create_orders(primary_question, non_primary_questions, grid_group)
        return grid_group

    def _create_grid(self, primary_question, non_primary_questions):
        attributes = self._get_grid_attributes()
        grid_group = primary_question.question_group.create(**attributes)
        grid_group.question.add(*non_primary_questions)
        return grid_group

    def _get_grid_attributes(self):
        order = self.subsection.next_group_order() if self.subsection else 0
        attributes ={'order': order, 'subsection': self.subsection, 'grid': True}
        attributes[self.cleaned_data.get('type')] = True
        return attributes

    def _create_orders(self, primary_question, non_primary_questions, grid_group):
        grid_group.orders.create(order=0, question=primary_question)
        for index, question in enumerate(non_primary_questions):
            grid_group.orders.create(order=index+1, question=question)