import os
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, View
from django.views.static import serve
from questionnaire.forms.sections import SectionForm
from questionnaire.forms.support_documents import SupportDocumentUploadForm
from questionnaire.models import SupportDocument, Questionnaire, Country
from questionnaire.services.users import UserQuestionnaireService


class UploadDocument(CreateView):
    model = SupportDocument
    template_name = 'questionnaires/entry/upload.html'
    form_class = SupportDocumentUploadForm
    success_url = None

    def get(self, request, *args, **kwargs):
        self.questionnaire = Questionnaire.objects.get(id=kwargs.get('questionnaire_id'))
        self.success_url = reverse('upload_document', args=(self.questionnaire.id, ))
        self.user_questionnaire_service = UserQuestionnaireService(self.country(), self.questionnaire)
        return super(UploadDocument, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.questionnaire = Questionnaire.objects.get(id=kwargs.get('questionnaire_id'))
        self.success_url = reverse('upload_document', args=(self.questionnaire.id, ))
        self.user_questionnaire_service = UserQuestionnaireService(self.country(), self.questionnaire)
        return super(UploadDocument, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UploadDocument, self).get_context_data(**kwargs)
        upload_data_initial = {'questionnaire': self.questionnaire, 'country': self.country()}
        attachments = self.user_questionnaire_service.attachments()
        context.update({'upload_form': self.form_class(initial=upload_data_initial),
                        'button_label': 'Upload', 'id': 'id-upload-form', 'questionnaire': self.questionnaire,
                        'action': reverse('upload_document', args=(self.questionnaire.id,)),
                        'documents': attachments,
                        'section_form': SectionForm(initial={'questionnaire': self.questionnaire}),
                        'ordered_sections': self.questionnaire.sections.order_by('order'),
                        'preview': self.user_questionnaire_service.preview(),
                        'new_section_action': reverse("new_section_page", args=(self.questionnaire.id,))})
        return context

    def form_valid(self, form):
        messages.success(self.request, "File was uploaded successfully")
        return super(UploadDocument, self).form_valid(form)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'upload_form': form,
                        'button_label': 'Upload', 'id': 'id-upload-form', 'questionnaire': self.questionnaire,
                        'documents': self.user_questionnaire_service.attachments(),
                        'ordered_sections': self.questionnaire.sections.order_by('order')})

    def country(self):
        country_id = self.request.GET.get('country', None)
        country = Country.objects.filter(id=country_id)
        country = country[0] if country.exists() else None
        return country or self.request.user.user_profile.country


class DownloadDocument(View):
    def get(self, *args, **kwargs):
        document = SupportDocument.objects.get(id=kwargs['document_id'], questionnaire=kwargs['questionnaire_id'])
        return serve(self.request, os.path.basename(document.path.url), os.path.dirname(document.path.url))


class DeleteDocument(View):
    model = SupportDocument

    def post(self, *args, **kwargs):
        document = self.model.objects.get(pk=kwargs['document_id'])
        questionnaire = document.questionnaire
        os.system("rm %s" % document.path.url)
        document.delete()
        messages.success(self.request, "Attachment was deleted successfully")
        return HttpResponseRedirect(reverse('upload_document', args=(questionnaire.id,)))