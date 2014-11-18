from django.db import models
from model_utils.managers import InheritanceManager

from questionnaire.models.base import BaseModel
from questionnaire.models import Question, QuestionOption, SubSection


class SkipRule(BaseModel):
    root_question = models.ForeignKey(Question, blank=False, null=False, related_name="root_skip_rules")
    response = models.ForeignKey(QuestionOption, blank=False, null=False, related_name="skip_rules")
    subsection = models.ForeignKey(SubSection, blank=False, null=False, related_name="skip_rules")

    objects = InheritanceManager()

    def get_question_group(self):
        groups = filter(lambda group: self.root_question in group.question.all(), self.subsection.question_group.all())
        if len(groups) == 1:
            return groups[0]
        else:
            raise Exception("Cannot find the question group for the root question")

    def get_sub_type(self):
        return self.__class__.__name__

    def copy_to(self, new_subsection, new_subsection_to_skip):
        raise NotImplementedError


class SkipQuestion(SkipRule):
    skip_question = models.ForeignKey(Question, blank=False, null=False, related_name="skip_rules")

    def copy_to(self, new_subsection, new_subsection_to_skip):
        SkipQuestion.objects.create(skip_question=self.skip_question, response=self.response,
                                    root_question=self.root_question, subsection=new_subsection)

    def is_in_hybrid_grid(self):
        return self.get_question_group().parent_group().hybrid

    def to_dictionary(self):
        return {'id': self.id,
                'skip_question': self.skip_question.text,
                'root_question': self.root_question.text,
                'response': self.response.text}


class SkipSubsection(SkipRule):
    skip_subsection = models.ForeignKey(SubSection, blank=False, null=False)

    def copy_to(self, new_subsection, new_subsection_to_skip):
        SkipSubsection.objects.create(skip_subsection=new_subsection_to_skip, response=self.response,
                                      root_question=self.root_question, subsection=new_subsection)

    def to_dictionary(self):
        return {'id': self.id,
                'skip_subsection': (" %s. %s" % (self.skip_subsection.order, self.skip_subsection.title)),
                'root_question': self.root_question.text,
                'response': self.response.text}
