import copy
from django.db import transaction

from questionnaire.models import QuestionGroupOrder, Questionnaire, SkipRule, SubSection
from questionnaire.models.skip_rule import SkipQuestion, SkipSubsection
from questionnaire.utils.cloner_util import create_copies


class QuestionnaireClonerService(object):
    def __init__(self, questionnaire, region=None):
        self.questionnaire = copy.deepcopy(questionnaire)
        self.region = region
        self.original_questionnaire = self._set_questionnaire_status(questionnaire)
        self.sections = None
        self.sub_sections = None
        self.question_groups = None

    @transaction.commit_on_success
    def clone(self):
        self.questionnaire.pk = None
        self.questionnaire.status = Questionnaire.DRAFT
        self.questionnaire.region = self.region
        self.questionnaire.parent = self.original_questionnaire
        self.questionnaire.save()
        self.sections = self._clone_sections()
        self.sub_sections = self._clone_sub_sections()
        self._clone_skip_rules()
        self.question_groups = self._clone_question_groups()
        self._assign_sub_groups()
        self._assign_questions_to_groups()
        return self.questionnaire, self.original_questionnaire

    def _set_questionnaire_status(self, questionnaire):
        if self.region:
            questionnaire.status = Questionnaire.PUBLISHED
            questionnaire.save()
        return questionnaire

    def _clone_sections(self):
        sections = self.original_questionnaire.sections.all()
        fields = ['name', 'title', 'description', 'order', 'is_core']
        return create_copies(sections, self.region, fields, questionnaire=self.questionnaire)

    def _clone_skip_rules_for_subsection(self, rules, new_subsection):
        map(lambda rule: rule.copy_to(new_subsection, self._get_new_subsection_by(rule)), rules)

    def _get_new_subsection_by(self, rule):
        skip_subsection_id = rule.__dict__.get('skip_subsection_id', None)
        if skip_subsection_id:
            subsection = SubSection.objects.get(id=skip_subsection_id)
            return self.sub_sections.get(subsection, None)
        return None

    def _clone_skip_rules(self):
        map(lambda (old, new): self._clone_skip_rules_for_subsection(old.skip_rules.all().select_subclasses(), new),
            self.sub_sections.iteritems())

    def _clone_sub_sections(self):
        sub_sections_map = {}
        fields = ['title', 'description', 'order', 'is_core']
        for old_section, new_section in self.sections.items():
            sub_sections = old_section.sub_sections.all()
            sub_sections_map.update(create_copies(sub_sections, self.region, fields, section=new_section))
        return sub_sections_map

    def _clone_question_groups(self):
        question_groups_map = {}
        fields = ['name', 'instructions', 'parent', 'order', 'allow_multiples', 'grid', 'display_all', 'hybrid']
        for old_sub_section, new_sub_section in self.sub_sections.items():
            question_groups = old_sub_section.all_question_groups()
            question_groups_map.update(create_copies(question_groups, self.region, fields, subsection=new_sub_section))
        return question_groups_map

    def _assign_sub_groups(self):
        for old_group, new_group in self.question_groups.items():
            if old_group.parent:
                new_group.parent = self.question_groups.get(old_group.parent)
                new_group.save()

    def _assign_questions_to_groups(self):
        for old_group, new_group in self.question_groups.items():
            new_group.question.add(*old_group.all_questions())
            if not old_group.parent:
                for order in old_group.question_orders():
                    QuestionGroupOrder.objects.create(order=order.order,
                                                      question_group=self.question_groups.get(old_group),
                                                      question=order.question)