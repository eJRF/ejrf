from django.db import models, IntegrityError
from questionnaire.models.base import BaseModel
from questionnaire.utils.model_utils import largest_uid, stringify


class Question(BaseModel):
    NUMBER = "Number"
    MULTICHOICE = "MultiChoice"
    DAY_MONTH_YEAR = "DD/MM/YYYY"
    MONTH_YEAR = "MM/YYYY"
    DECIMAL = 'decimal'
    INTEGER = 'integer'
    DATE = "Date"

    DATE_SUB_TYPES = (
        ("DD/MM/YYYY", DAY_MONTH_YEAR),
        ("MM/YYYY", MONTH_YEAR),
        (DECIMAL, 'Decimal'),
        (INTEGER, 'Integer')
    )
    ANSWER_TYPES = (
        ("Date", DATE),
        ("MultiChoice", MULTICHOICE),
        ("Number", NUMBER),
        ("Text", "Text"),
    )

    text = models.TextField(blank=False, null=False)
    export_label = models.TextField(blank=True, null=False)
    instructions = models.TextField(blank=True, null=True)
    UID = models.CharField(blank=False, null=False, max_length=6)
    
    answer_type = models.CharField(blank=False, null=False, max_length=20, choices=ANSWER_TYPES)
    answer_sub_type = models.CharField(blank=True, null=True, max_length=20, choices=DATE_SUB_TYPES)

    region = models.ForeignKey("Region", blank=False, null=True, related_name="questions")
    theme = models.ForeignKey("Theme", null=True, related_name="questions")
    is_primary = models.BooleanField(blank=False, null=False, default=False)
    is_required = models.BooleanField(blank=False, null=False, default=False)
    parent = models.ForeignKey("Question", blank=False, null=True, related_name="child")

    def save(self, *args, **kwargs):
        if self.parent:
            self.UID = self.parent.UID
            return super(Question, self).save(*args, **kwargs)
        questions_with_same_uid = Question.objects.filter(UID=self.UID)
        if questions_with_same_uid.exists() and not self._editing(questions_with_same_uid[0]):
            raise IntegrityError("Question with UID %s already exists and is not a parent of this question." % self.UID)
        return super(Question, self).save(*args, **kwargs)

    def _editing(self, question):
        return self.id == question.id

    def all_answers(self):
        return self.answers.filter(status='Submitted').order_by('answergroup__id').select_subclasses()

    @property
    def is_core(self):
        return not self.region

    def __unicode__(self):
        return "%s" % self.text

    def group(self):
        return self.question_group.all()[0]

    def is_first_in_group(self):
        questions = self.group().ordered_questions()
        return self == questions[0]

    def is_last_in_group(self):
        questions = self.group().ordered_questions()
        return self == questions[-1]

    def has_question_option_instructions(self):
        return self.options.exclude(instructions=None)

    def latest_answer(self, parent_group, country, version=1):
        answer = self.answers.filter(answergroup__grouped_question=parent_group,
                                     country=country, version=version).select_subclasses()
        if answer.exists():
            return answer.latest('modified')
        return None

    def is_in_subgroup(self):
        return self.question_group.exclude(parent=None).exists()

    def can_be_deleted(self):
        return not self.all_answers().exists()

    def question_groups_in(self, questionnaire):
        return self.question_group.filter(subsection__section__questionnaire=questionnaire)

    def is_assigned_to(self, questionnaire):
        return self.question_groups_in(questionnaire).exists()

    def questionnaires(self):
        from questionnaire.models import Questionnaire

        return Questionnaire.objects.filter(sections__sub_sections__question_group__in=self.question_group.all())

    def is_multichoice(self):
        return self.answer_type == self.MULTICHOICE

    def answered_options(self, question_group, **kwargs):
        all_answers = self.answers.filter(answergroup__grouped_question=question_group, **kwargs). \
            order_by('modified').distinct().select_subclasses()
        return [answer.response for answer in all_answers]

    @classmethod
    def next_uid(cls):
        return stringify(largest_uid(cls) + 1)


class QuestionOption(BaseModel):
    text = models.CharField(max_length=100, blank=False, null=False)
    question = models.ForeignKey(Question, related_name="options")
    instructions = models.TextField(blank=True, null=True)
    UID = models.CharField(blank=False, max_length=6, unique=True, null=True)

    def __unicode__(self):
        return "%s" % self.text

    @classmethod
    def generate_uid(cls):
        latest = cls.objects.exclude(UID=None)
        if latest.exists():
            latest = latest.latest('modified').UID
            return '%s%d' % (latest[:-1], int(latest[-1]) + 1)
        return None

    class Meta:
        ordering = ('modified',)
        app_label = 'questionnaire'