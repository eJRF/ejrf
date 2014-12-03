from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from questionnaire.forms.assign_question import AssignQuestionForm
from questionnaire.mixins import RegionAndPermissionRequiredMixin
from questionnaire.models import SubSection, Question
from questionnaire.models.skip_rule import SkipQuestion


class AssignQuestion(RegionAndPermissionRequiredMixin, View):
    template_name = "questionnaires/assign_questions.html"
    permission_required = 'auth.can_edit_questionnaire'

    def get(self, request, *args, **kwargs):
        subsection = SubSection.objects.select_related('section').get(id=kwargs['subsection_id'])
        region = request.user.user_profile.region
        form = AssignQuestionForm(subsection=subsection, region=region)
        active_questions = subsection.section.questionnaire.get_all_questions()
        questions = form.fields['questions'].queryset.filter(child=None)
        if 'hide' in request.GET:
            questions = questions.exclude(id__in=[question.id for question in active_questions])
        context = {'assign_question_form': form, 'active_questions': active_questions,
                   'btn_label': 'Done', 'questions': questions, 'subsection': subsection}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        referer_url = request.META.get('HTTP_REFERER', None)
        subsection = SubSection.objects.get(id=kwargs['subsection_id'])
        region = request.user.user_profile.region
        form = AssignQuestionForm(request.POST, subsection=subsection, region=region)
        if form.is_valid():
            form.save()
            messages.success(request, "Questions successfully assigned to questionnaire.")
            return HttpResponseRedirect(referer_url)
        questions = form.fields['questions'].queryset.filter(child=None)
        context = {'assign_question_form': form,
                   'btn_label': 'Done', 'questions': questions}
        return render(request, self.template_name, context)


class UnAssignQuestion(RegionAndPermissionRequiredMixin, View):
    permission_required = 'auth.can_edit_questionnaire'

    def post(self, request, *args, **kwargs):
        referer_url = request.META.get('HTTP_REFERER', None)
        subsection = SubSection.objects.get(id=kwargs['subsection_id'])
        question = Question.objects.get(id=kwargs['question_id'])
        groups_in_subsection = subsection.question_group.all()
        question.question_group.remove(*groups_in_subsection)
        question.orders.filter(question_group__in=groups_in_subsection).delete()
        skip_questions = SkipQuestion.objects.filter(Q(skip_question=question) | Q(root_question=question))
        if skip_questions.exists():
            skip_questions.delete()

        messages.success(request, "Question successfully unassigned from questionnaire.")
        return HttpResponseRedirect(referer_url)
