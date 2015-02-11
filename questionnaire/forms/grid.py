from django import forms
from django.db.models import Q

from questionnaire.forms.custom_widgets import MultiChoiceQuestionSelectWidget
from questionnaire.models import Question, QuestionGroup


GRID_TYPES = (('', 'Choose One'),
              ('display_all', 'Display All'),
              ('allow_multiples', 'Add More'),
              ('hybrid', 'Hybrid'))


class GridForm(forms.Form):
    type = forms.ChoiceField(choices=GRID_TYPES)
    primary_question = forms.ModelChoiceField(queryset=None, empty_label='Choose One',
                                              widget=MultiChoiceQuestionSelectWidget())
    columns = forms.ModelMultipleChoiceField(queryset=None, widget=forms.SelectMultiple(attrs={'class': 'hide'}))
    subgroup = forms.ModelMultipleChoiceField(queryset=None, widget=forms.SelectMultiple(attrs={'class': 'hide'}),
                                              required=False)

    def __init__(self, *args, **kwargs):
        self.subsection = kwargs.pop('subsection', None)
        self.region = kwargs.pop('region', None)
        self.instance = kwargs.pop('instance', None)
        super(GridForm, self).__init__(*args, **kwargs)
        unused_regional_questions = self.unused_regional_questions()
        self.fields['primary_question'].queryset = unused_regional_questions.filter(is_primary=True)
        non_primary_questions = unused_regional_questions.exclude(is_primary=True)
        self.fields['columns'].queryset = non_primary_questions
        self.fields['subgroup'].queryset = non_primary_questions

    def unused_regional_questions(self):
        questions = Question.objects.filter(region=self.region)
        if self.subsection:
            questionnaire = self.subsection.section.questionnaire
            questions = questions.exclude(question_group__subsection__section__questionnaire=questionnaire).distinct()
        return questions

    def clean(self):
        cleaned_data = super(GridForm, self).clean()
        type = cleaned_data.get('type')
        primary_question = cleaned_data.get('primary_question')
        if not type or not primary_question:
            return cleaned_data
        self._clean_multichoice_(primary_question, type)
        self._clean_('columns', primary_question.theme)
        self._clean_('subgroup', primary_question.theme)
        return cleaned_data

    def _clean_multichoice_(self, primary_question, type_):
        if not primary_question.is_multichoice() and type_ == 'display_all':
            message = 'This type of grid requires a multichoice primary question.'
            self._errors['primary_question'] = self.error_class([message])
            del self.cleaned_data['primary_question']

    def _clean_(self, fieldname, theme):
        field = self.cleaned_data.get(fieldname, None)
        if field:
            fields_with_different_themes = field.exclude(theme=theme)
            if fields_with_different_themes:
                message = 'All questions must be with theme %s.' % theme.name
                self._errors[fieldname] = self.error_class([message])
                del self.cleaned_data[fieldname]

    def save(self):
        primary_question = self.cleaned_data.get('primary_question')
        non_primary_questions = self.cleaned_data.get('columns')
        sub_group_questions = self.cleaned_data.get('subgroup')
        grid_group = self._create_grid(primary_question, non_primary_questions, sub_group_questions)
        self._create_orders(primary_question, non_primary_questions, grid_group)
        return grid_group

    def _create_grid(self, primary_question, non_primary_questions, sub_group_questions):
        sub_group_ids = sub_group_questions.values_list('id', flat=True)
        remaining_questions = non_primary_questions.exclude(id__in=sub_group_ids)
        parent_grid_group = self._create_parent_grid(primary_question, remaining_questions)
        self._create_grid_sub_group(parent_grid_group, sub_group_questions)
        return parent_grid_group

    def _create_grid_sub_group(self, parent_grid_group, sub_group_questions):
        if sub_group_questions:
            group = parent_grid_group.sub_group.create(grid=True, subsection=self.subsection)
            group.question.add(*sub_group_questions)

    def _create_parent_grid(self, primary_question, remaining_questions):
        attributes = self._get_grid_attributes()
        grid_group = self.instance or QuestionGroup.objects.create(**attributes)

        grid_group.question.add(primary_question)
        grid_group.question.add(*remaining_questions)
        return grid_group

    def _get_grid_attributes(self):
        order = self.subsection.next_group_order() if self.subsection else 0
        attributes = {'order': order, 'subsection': self.subsection, 'grid': True, 'is_core': not self.region}
        type_ = self.cleaned_data.get('type')
        attributes[type_] = True
        if type_ == 'hybrid':
            attributes['allow_multiples'] = True
        return attributes

    def _create_orders(self, primary_question, non_primary_questions, grid_group):
        grid_group.orders.create(order=0, question=primary_question)
        question_ids = self.data.getlist('columns') if hasattr(self.data, 'getlist') else self.data.get('columns')
        for index, question_id in enumerate(question_ids):
            question = filter(lambda question: question.id == int(question_id), non_primary_questions)
            grid_group.orders.create(order=index + 1, question=question[0])


class EditGridForm(GridForm):

    def save(self):
        self.instance.orders.all().delete()
        self.instance.sub_group.all().delete()
        self.instance.question.clear()
        return super(EditGridForm, self).save()

    def unused_regional_questions(self):
        questions = Question.objects.filter(region=self.region)
        if self.subsection:
            instance_question_ids = self.instance.question.values_list('id', flat=True)
            questionnaire = self.subsection.section.questionnaire
            questions = questions.exclude(Q(question_group__subsection__section__questionnaire=questionnaire),
                                          ~Q(id__in=instance_question_ids)).distinct()

            print instance_question_ids
        return questions
