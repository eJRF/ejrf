from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from questionnaire.forms.grid import GridForm
from questionnaire.mixins import RegionAndPermissionRequiredMixin
from questionnaire.models import SubSection, QuestionGroup
from questionnaire.utils.model_utils import reindex_orders_in


class CreateGrid(RegionAndPermissionRequiredMixin, View):
    template_name = "questionnaires/grid/new.html"
    permission_required = 'auth.can_edit_questionnaire'

    def get(self, request, *args, **kwargs):
        subsection = SubSection.objects.select_related('section').get(id=kwargs['subsection_id'])
        region = request.user.user_profile.region
        form = GridForm(subsection=subsection, region=region)
        context = {'grid_form': form, 'non_primary_questions': form.fields['columns'].queryset,
                   'btn_label': 'Create', 'subsection': subsection, 'id': 'create_grid_form',
                   'class': 'create-grid-form', }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        referer_url = request.META.get('HTTP_REFERER', None)
        subsection = SubSection.objects.get(id=kwargs['subsection_id'])
        region = request.user.user_profile.region
        form = GridForm(request.POST, subsection=subsection, region=region)
        if form.is_valid():
            form.save()
            messages.success(request, "Grid successfully created.")
            return HttpResponseRedirect(referer_url)
        context = {'grid_form': form, 'non_primary_questions': form.fields['columns'].queryset,
                   'btn_label': 'Create', 'subsection': subsection, 'id': 'create_grid_form',
                   'class': 'create-grid-form', }
        messages.error(request, "Grid NOT created. See errors below.")
        return render(request, self.template_name, context)


class DeleteGrid(RegionAndPermissionRequiredMixin, View):
    permission_required = 'auth.can_edit_questionnaire'

    def post(self, request, *args, **kwargs):
        referer_url = request.META.get('HTTP_REFERER', None)
        subsection = SubSection.objects.get(id=kwargs['subsection_id'])
        QuestionGroup.objects.filter(id=kwargs['questionGroup_id']).delete()
        reindex_orders_in(QuestionGroup, subsection=subsection)
        messages.success(request, "Grid successfully removed from questionnaire.")
        return HttpResponseRedirect(referer_url)
