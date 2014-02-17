from braces.views import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import CreateView

from questionnaire.forms.sections import SectionForm, SubSectionForm
from questionnaire.models import Section, SubSection


class NewSection(PermissionRequiredMixin, CreateView):
    permission_required = 'auth.can_view_users'

    def __init__(self, **kwargs):
        super(NewSection, self).__init__(**kwargs)
        self.form_class = SectionForm
        self.object = Section
        self.template_name = "sections/subsections/new.html"

    def get_context_data(self, **kwargs):
        context = super(NewSection, self).get_context_data(**kwargs)
        context['btn_label'] = "CREATE"
        return context

    def form_valid(self, form):
        section = form.save(commit=False)
        section.order = Section.get_next_order(form.cleaned_data['questionnaire'])
        section.save()
        messages.success(self.request,"Section created successfully" )
        return super(NewSection, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,"Section NOT created. See errors below." )
        context = {'id':  "new-section-modal",
                   'form': form, 'btn_label': "CREATE", }
        return self.render_to_response(context)


class NewSubSection(PermissionRequiredMixin, CreateView):
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
        section = Section.objects.get(id=section_id)
        self.form = SubSectionForm(instance=SubSection(section=section), data=request.POST)
        self.referer_url = reverse('questionnaire_entry_page', args=(questionnaire_id, section_id))
        if self.form.is_valid():
            return self._form_valid()
        return self._form_invalid()

    def _form_valid(self):
        self.form.save()
        messages.success(self.request, "Subsection successfully created." )
        return HttpResponseRedirect(self.referer_url)

    def _form_invalid(self):
        messages.error(self.request, "Subsection NOT created. See errors below." )
        context = {'id':  "new-subsection-modal",
                   'form': self.form, 'btn_label': "CREATE", }
        return self.render_to_response(context)