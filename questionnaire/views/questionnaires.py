from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import FormView
from django.views.generic import View
from braces.views import MultiplePermissionsRequiredMixin, PermissionRequiredMixin

from questionnaire.forms.questionnaires import QuestionnaireFilterForm, PublishQuestionnaireForm
from questionnaire.forms.sections import SectionForm, SubSectionForm
from questionnaire.mixins import AdvancedMultiplePermissionsRequiredMixin, DoesNotExistExceptionHandlerMixin
from questionnaire.services.questionnaire_cloner import QuestionnaireClonerService
from questionnaire.services.questionnaire_finalizer import QuestionnaireFinalizeService
from questionnaire.services.questionnaire_entry_form_service import QuestionnaireEntryFormService
from questionnaire.models import Questionnaire, Section, QuestionGroup, Answer
from questionnaire.forms.answers import NumericalAnswerForm, TextAnswerForm, DateAnswerForm, MultiChoiceAnswerForm
from questionnaire.services.users import UserQuestionnaireService
from questionnaire.utils.service_utils import filter_empty_values
from questionnaire.utils.view_utils import get_country, get_questionnaire_status, get_regions


ANSWER_FORM = {'Number': NumericalAnswerForm,
               'Text': TextAnswerForm,
               'Date': DateAnswerForm,
               'MultiChoice': MultiChoiceAnswerForm,
}


class Entry(DoesNotExistExceptionHandlerMixin, AdvancedMultiplePermissionsRequiredMixin, FormView):
    template_name = 'questionnaires/entry/index.html'
    model = Questionnaire
    GET_permissions = {'any': ('auth.can_submit_responses', 'auth.can_view_users', 'auth.can_edit_questionnaire')}
    POST_permissions = {'any': ('auth.can_submit_responses', )}

    def get(self, request, *args, **kwargs):
        query_params = {'id': self.kwargs['questionnaire_id'],
                        'region__in': get_regions(request), 'status__in': get_questionnaire_status(request)}
        query_params = filter_empty_values(query_params)
        questionnaire = Questionnaire.objects.get(**query_params)
        section = Section.objects.get(id=self.kwargs['section_id'])
        country = get_country(self.request)
        self.user_questionnaire_service = UserQuestionnaireService(country, questionnaire, request.GET.get("version"))
        get_version = self.user_questionnaire_service.GET_version
        initial = {'status': 'Draft', 'country': country,
                   'version': get_version, 'questionnaire': questionnaire}
        required_answers = 'show' in request.GET
        formsets = QuestionnaireEntryFormService(section, initial=initial, highlight=required_answers,
                                                 edit_after_submit=self.user_questionnaire_service.edit_after_submit)
        printable = 'printable' in request.GET
        version = request.GET.get('version', None)
        preview = self._check_preview_mode(questionnaire)
        region = self.request.user.user_profile.region
        context = {'questionnaire': questionnaire,
                   'section': section, 'printable': printable,
                   'preview': preview, 'formsets': formsets,
                   'ordered_sections': questionnaire.sections.order_by('order'),
                   'section_form': SectionForm(initial={'questionnaire': questionnaire, 'region': region}),
                   'new_section_action': reverse('new_section_page', args=(questionnaire.id, )),
                   'subsection_form': SubSectionForm(),
                   'subsection_action': reverse('new_subsection_page', args=(questionnaire.id, section.id)),
                   'the_version': version or get_version,
                   'country': country,
                   'documents': self.user_questionnaire_service.attachments()}
        # slow in some instances take 1.5 secs
        return self.render_to_response(context)

    def _check_preview_mode(self, questionnaire):
        user = self.request.user
        perm = None
        if user.has_perm('auth.can_edit_questionnaire'):
            perm = questionnaire.is_finalized() or questionnaire.is_published()
        return perm or self.user_questionnaire_service.preview() or 'preview' in self.request.GET

    def post(self, request, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(id=self.kwargs['questionnaire_id'])
        section = Section.objects.get(id=self.kwargs['section_id'])
        user_questionnaire_service = UserQuestionnaireService(self.request.user.user_profile.country, questionnaire)
        initial = {'country': self.request.user.user_profile.country, 'status': 'Draft',
                   'version': user_questionnaire_service.POST_version, 'questionnaire': questionnaire}
        formsets = QuestionnaireEntryFormService(section, initial=initial, data=request.POST,
                                                 edit_after_submit=user_questionnaire_service.edit_after_submit)

        context = {'questionnaire': questionnaire, 'section': section,
                   'formsets': formsets, 'ordered_sections': questionnaire.ordered_sections(),
                   'form': SectionForm(initial={'questionnaire': questionnaire}),
                   'new_section_action': reverse('new_section_page', args=(questionnaire.id, )),
                   'subsection_form': SubSectionForm(),
                   'subsection_action': reverse('new_subsection_page', args=(questionnaire.id, section.id)),
                   'documents': user_questionnaire_service.attachments()}

        if formsets.is_valid():
            return self._form_valid(request, formsets, context)
        return self._form_invalid(request, context)

    def _form_valid(self, request, formsets, context):
        formsets.save()
        message = 'Draft saved.'
        messages.success(request, message)
        if request.POST.get('redirect_url', None):
            return HttpResponseRedirect(request.POST['redirect_url'].replace('preview=1', ''))
        return self.render_to_response(context)

    def _form_invalid(self, request, context):
        message = 'Draft NOT saved. See errors below.'
        messages.error(request, message)
        return self.render_to_response(context)


class SubmitQuestionnaire(AdvancedMultiplePermissionsRequiredMixin, View):
    GET_permissions = {'any': ('auth.can_submit_responses', 'auth.can_view_users', 'auth.can_edit_questionnaire')}
    POST_permissions = {'any': ('auth.can_submit_responses', )}

    def post(self, request, *args, **kwargs):
        user_country = self.request.user.user_profile.country
        questionnaire = Questionnaire.objects.get(id=self.kwargs['questionnaire_id'])
        user_questionnaire = UserQuestionnaireService(user_country, questionnaire)
        if not user_questionnaire.required_sections_answered():
            return self._reload_section_with_required_answers_errors(request, user_questionnaire, *args, **kwargs)
        return self._submit_answers(request, user_questionnaire, *args, **kwargs)

    def _submit_answers(self, request, user_questionnaire_service, *args, **kwargs):
        user_questionnaire_service.submit()
        referer_url = request.META.get('HTTP_REFERER', None)
        redirect_url = referer_url or reverse('home_page')
        redirect_url = self._format_redirect_url(redirect_url, referer_url)
        messages.success(request, 'Questionnaire Submitted.')
        return HttpResponseRedirect(redirect_url)

    def _reload_section_with_required_answers_errors(self, request, user_questionnaire_service, *args, **kwargs):
        section = user_questionnaire_service.unanswered_section
        questionnaire = user_questionnaire_service.questionnaire
        messages.error(request, 'Questionnaire NOT submitted. See errors below.')
        redirect_url = reverse('questionnaire_entry_page', args=(questionnaire.id, section.id))
        return HttpResponseRedirect('%s?show=errors' % redirect_url)

    def _format_redirect_url(self, redirect_url, referer_url):
        redirect_url = redirect_url.replace('?show=errors', '')
        if referer_url and referer_url.endswith('?preview=1'):
            return redirect_url
        return "%s?preview=1" % redirect_url


class DuplicateQuestionnaire(MultiplePermissionsRequiredMixin, View):
    permissions = {'any': ('auth.can_view_users',)}

    def post(self, *args, **kwargs):
        form = QuestionnaireFilterForm(self.request.POST)
        if form.is_valid():
            duplicate, _ = QuestionnaireClonerService(form.cleaned_data['questionnaire']).clone()
            duplicate.name = form.cleaned_data['name']
            duplicate.year = form.cleaned_data['year']
            duplicate.save()
            message = "The questionnaire has been duplicated successfully, You can now go ahead and edit it"
            messages.success(self.request, message)
            redirect_url = reverse('questionnaire_entry_page', args=(duplicate.id, duplicate.sections.all()[0].id))
            return HttpResponseRedirect(redirect_url)
        message = "Questionnaire could not be duplicated see errors below"
        messages.error(self.request, message)
        return HttpResponseRedirect(reverse('manage_jrf_page'))


class FinalizeQuestionnaire(MultiplePermissionsRequiredMixin, View):
    permissions = {'any': ('auth.can_view_users', 'auth.can_edit_questionnaire')}

    def post(self, request, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(id=kwargs['questionnaire_id'])
        message = QuestionnaireFinalizeService(questionnaire).finalize()
        messages.success(self.request, message)
        referer_url = request.META['HTTP_REFERER']
        return HttpResponseRedirect(referer_url)


class UnfinalizeQuestionnaire(MultiplePermissionsRequiredMixin, View):
    permissions = {'any': ('auth.can_view_users', 'auth.can_edit_questionnaire')}

    def post(self, request, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(id=kwargs['questionnaire_id'])
        message = QuestionnaireFinalizeService(questionnaire).unfinalize()
        messages.success(self.request, message)
        referer_url = request.META.get('HTTP_REFERER', None) or reverse('manage_jrf_page')
        return HttpResponseRedirect(referer_url)


class PublishQuestionnaire(PermissionRequiredMixin, View):
    permission_required = 'auth.can_view_users'

    template_name = 'questionnaires/_publish.html'

    def get(self, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(id=kwargs['questionnaire_id'])
        form = PublishQuestionnaireForm(initial={'questionnaire': questionnaire})
        context = {'questionnaire': questionnaire,
                   'publish_form': form, 'btn_label': "Publish",
                   'cancel_url': reverse('manage_jrf_page')}
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(id=kwargs['questionnaire_id'])
        form = PublishQuestionnaireForm(initial={'questionnaire': questionnaire}, data=self.request.POST)
        if form.is_valid():
            form.save()
            regions = map(lambda _region: _region.name, form.cleaned_data['regions'])
            message = "The questionnaire has been published to %s" % ", ".join([region for region in sorted(regions)])
            messages.success(self.request, message)
            return HttpResponseRedirect(reverse('manage_jrf_page'))
        else:
            message = "Questionnaire could not be published see errors below"
            messages.error(self.request, message)
        context = {'questionnaire': questionnaire, 'publish_form': form, 'btn_label': "Publish",
                   'cancel_url': reverse('manage_jrf_page')}
        return render(self.request, self.template_name, context)


class ApproveQuestionnaire(MultiplePermissionsRequiredMixin, View):
    permissions = {'any': ('auth.can_view_users',)}
    template_name = 'base/modals/_confirm.html'

    def get(self, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(id=kwargs['questionnaire_id'])
        context = {'questionnaire': questionnaire, 'btn_label': "Approve",
                   'cancel_url': reverse('manage_jrf_page')}
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(id=kwargs['questionnaire_id'])
        message = QuestionnaireFinalizeService(questionnaire).approve()
        messages.success(self.request, message)
        referer_url = request.META['HTTP_REFERER']
        return HttpResponseRedirect(referer_url)


class DeleteAnswerRow(PermissionRequiredMixin, View):
    permission_required = 'auth.can_submit_responses'

    def post(self, request, *args, **kwargs):
        group = QuestionGroup.objects.get(id=kwargs['group_id'])
        primary_answer_id = request.POST.get('primary_answer')
        primary_answer = Answer.objects.filter(id=primary_answer_id).select_subclasses()
        country = self.request.user.user_profile.country
        if primary_answer[0].can_be_deleted(group, country):
            self._delete_answer_row(primary_answer, group)
        return HttpResponse()

    @staticmethod
    def _delete_answer_row(primary_answer, group):
        answergroup_filter = primary_answer[0].answergroup.filter(grouped_question=group)
        answergroup_filter[0].answer.all().delete()
        answergroup_filter.delete()
