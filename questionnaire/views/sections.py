import json

from braces.views import PermissionRequiredMixin
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import CreateView, UpdateView, DeleteView, View
from django.utils.cache import add_never_cache_headers

from questionnaire.forms.sections import SectionForm, SubSectionForm
from questionnaire.mixins import RegionAndPermissionRequiredMixin, DoesNotExistExceptionHandlerMixin, \
    OwnerAndPermissionRequiredMixin
from questionnaire.models import Section, SubSection, QuestionGroup, Questionnaire
from questionnaire.services.question_re_indexer import QuestionReIndexer, OrderBasedReIndexer, GridReorderer
from questionnaire.utils.model_utils import reindex_orders_in


class NewSection(RegionAndPermissionRequiredMixin, CreateView):
    permission_required = 'auth.can_edit_questionnaire'

    def __init__(self, **kwargs):
        super(NewSection, self).__init__(**kwargs)
        self.form_class = SectionForm
        self.object = Section
        self.questionnaire = None
        self.template_name = "sections/subsections/new.html"

    def post(self, request, *args, **kwargs):
        self.questionnaire = Questionnaire.objects.get(id=kwargs['questionnaire_id'])
        return super(NewSection, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NewSection, self).get_context_data(**kwargs)
        context['btn_label'] = "CREATE"
        return context

    def get_initial(self):
        initial = super(NewSection, self).get_initial()
        profile = self.request.user.user_profile
        initial.update({'questionnaire': self.questionnaire, 'region': profile.region, 'user': profile.user})
        return initial

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Section created successfully")
        return super(NewSection, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Section NOT created. See errors below.")
        context = {'id': "new-section-modal",
                   'form': form, 'btn_label': "CREATE", }
        return self.render_to_response(context)


class EditSection(OwnerAndPermissionRequiredMixin, UpdateView):
    permission_required = 'auth.can_edit_questionnaire'

    def __init__(self, *args, **kwargs):
        super(EditSection, self).__init__(*args, **kwargs)
        self.form_class = SectionForm
        self.model = Section
        self.template_name = "sections/subsections/new.html"
        self.pk_url_kwarg = 'section_id'

    def get_context_data(self, **kwargs):
        context = super(EditSection, self).get_context_data(**kwargs)
        context['btn_label'] = "SAVE"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Section updated successfully.")
        return super(EditSection, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Section NOT updated. See errors below.")
        return super(EditSection, self).form_invalid(form)


class DeleteSection(DoesNotExistExceptionHandlerMixin, OwnerAndPermissionRequiredMixin, DeleteView):
    permission_required = 'auth.can_edit_questionnaire'

    def __init__(self, *args, **kwargs):
        super(DeleteSection, self).__init__(*args, **kwargs)
        self.model = Section
        self.object = None
        self.pk_url_kwarg = 'section_id'
        self.success_url = reverse("home_page")
        self.section = None

    def get_success_url(self):
        referer_url = self.request.META.get('HTTP_REFERER', None)
        section_page = reverse("questionnaire_entry_page", args=(self.section.questionnaire.id, self.section.id))
        deleting_myself = referer_url and (section_page in referer_url)
        if deleting_myself:
            return self.section.questionnaire.absolute_url()
        if referer_url:
            return referer_url
        return self.success_url

    def post(self, request, *args, **kwargs):
        self.section = self.get_object()
        user_profile = self.request.user.user_profile
        if user_profile.can_delete(self.section):
            response = super(DeleteSection, self).post(request, *args, **kwargs)
            reindex_orders_in(Section, questionnaire=self.section.questionnaire)
            message = "Section successfully deleted."
            messages.success(request, message)
            return response
        message = "You are not permitted to delete a core section"
        messages.error(request, message)
        return HttpResponseRedirect(self.section.get_absolute_url())


class NewSubSection(RegionAndPermissionRequiredMixin, CreateView):
    permission_required = 'auth.can_edit_questionnaire'

    def __init__(self, **kwargs):
        super(NewSubSection, self).__init__(**kwargs)
        self.object = SubSection
        self.form_class = SubSectionForm
        self.template_name = "sections/subsections/new.html"

    def get_context_data(self, **kwargs):
        context = super(NewSubSection, self).get_context_data(**kwargs)
        context['btn_label'] = "CREATE"
        return context

    def post(self, request, *args, **kwargs):
        questionnaire_id = kwargs.get('questionnaire_id')
        section_id = kwargs.get('section_id')
        self.section = Section.objects.get(id=section_id)
        self.form = SubSectionForm(instance=SubSection(section=self.section), data=request.POST, initial={'user': request.user})
        self.referer_url = reverse('questionnaire_entry_page', args=(questionnaire_id, section_id))
        if self.form.is_valid():
            return self._form_valid()

    def _form_valid(self):
        subsection = self.form.save(commit=False)
        subsection.order = SubSection.get_next_order(self.section.id)
        subsection.region = self.request.user.user_profile.region
        subsection.save()
        messages.success(self.request, "Subsection successfully created.")
        return HttpResponseRedirect(self.referer_url)


class EditSubSection(OwnerAndPermissionRequiredMixin, UpdateView):
    permission_required = 'auth.can_edit_questionnaire'

    def __init__(self, *args, **kwargs):
        super(EditSubSection, self).__init__(*args, **kwargs)
        self.form_class = SubSectionForm
        self.model = SubSection
        self.template_name = "sections/subsections/new.html"
        self.pk_url_kwarg = 'subsection_id'

    def get_context_data(self, **kwargs):
        context = super(EditSubSection, self).get_context_data(**kwargs)
        context['btn_label'] = "SAVE"
        return context

    def form_valid(self, form):
        messages.success(self.request, "SubSection updated successfully.")
        return super(EditSubSection, self).form_valid(form)


class DeleteSubSection(OwnerAndPermissionRequiredMixin, DeleteView):
    permission_required = 'auth.can_edit_questionnaire'

    def __init__(self, **kwargs):
        super(DeleteSubSection, self).__init__(**kwargs)
        self.model = SubSection
        self.pk_url_kwarg = 'subsection_id'
        self.success_url = "/"

    def _set_success_url(self):
        self.object = self.get_object()
        section = self.object.section
        return section.get_absolute_url()

    def post(self, request, *args, **kwargs):
        self.success_url = self._set_success_url()
        if request.user.user_profile.can_delete(self.object):
            response = super(DeleteSubSection, self).post(request, *args, **kwargs)
            reindex_orders_in(SubSection, section=self.object.section)
            message = "Subsection successfully deleted."
            messages.success(request, message)
            return response
        message = "You are not permitted to delete a core subsection"
        messages.error(request, message)
        return HttpResponseRedirect(self.object.get_absolute_url())


class GetSubSections(OwnerAndPermissionRequiredMixin, View):
    permission_required = 'auth.can_edit_questionnaire'

    def get(self, request, *args, **kwargs):
        section_id = kwargs.get("section_id")
        subsections = self._get_subsections(section_id, request)
        subsections_dict = map(lambda subsection: subsection.to_dict(), subsections)
        response = HttpResponse(json.dumps(subsections_dict), content_type="application/json", status=200)
        add_never_cache_headers(response)
        return response

    def _get_subsections(self, section_id, request):
        if request.user.user_profile.is_global_admin:
            return SubSection.objects.filter(section_id=section_id, region__isnull=True, is_core=True)
        return SubSection.objects.filter(section_id=section_id, region=request.user.user_profile.region, is_core=False)


class ReOrderQuestions(PermissionRequiredMixin, View):
    permission_required = 'auth.can_edit_questionnaire'

    def post(self, *args, **kwargs):
        sub_section = SubSection.objects.get(id=kwargs.get('subsection_id'))
        if self._no_questions_to_reorder():
            messages.warning(self.request, "There was nothing to re-order.")
            return HttpResponseRedirect(sub_section.get_absolute_url())

        QuestionReIndexer(self.request.POST).reorder_questions()
        messages.success(self.request, "The questions were reordered successfully")
        return HttpResponseRedirect(sub_section.get_absolute_url())

    def _no_questions_to_reorder(self):
        post_data = self.request.POST
        return len(post_data.keys()) <= 1 and 'csrfmiddlewaretoken' in post_data.keys()


class MoveSubsection(PermissionRequiredMixin, View):
    permission_required = 'auth.can_edit_questionnaire'

    def post(self, request, *args, **kwargs):
        subsection = SubSection.objects.get(id=request.POST.get('subsection'))
        order = request.POST.get('modal-subsection-position')
        indexer_response = OrderBasedReIndexer(subsection, order, section=subsection.section).reorder()
        messages.success(request, indexer_response)
        return HttpResponseRedirect(subsection.get_absolute_url())


class MoveGrid(PermissionRequiredMixin, View):
    permission_required = 'auth.can_edit_questionnaire'

    def post(self, request, *args, **kwargs):
        group_id = request.POST.get("group_id")
        move_direction = request.POST.get("move_direction")

        question_group = QuestionGroup.objects.get(id=group_id)
        grid_reorderer = GridReorderer(question_group, move_direction)
        grid_reorderer.reorder_group_in_sub_section()
        self.add_message(grid_reorderer.message)
        return HttpResponseRedirect(question_group.subsection.get_absolute_url())

    def add_message(self, reorder_messages):
        if 'warning' in reorder_messages.keys():
            messages.warning(self.request, reorder_messages.get('warning'))
        else:
            messages.success(self.request, reorder_messages.get('success'))
