import json
import os
import subprocess
import time
import urllib
import urlparse

from django.core.files import File
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from braces.views import LoginRequiredMixin

from questionnaire.forms.filter import ExportFilterForm
from questionnaire.models import Questionnaire, Country
from questionnaire.services.export_data_service import ExportToTextService
from questionnaire.utils.service_utils import filter_empty_values


class ExportToTextView(LoginRequiredMixin, TemplateView):
    ALL_QUESTIONNAIRES = "All Questionnaires"

    def __init__(self):
        super(ExportToTextView, self).__init__()
        self.template_name = "home/extract.html"

    def get_context_data(self, **kwargs):
        context = super(ExportToTextView, self).get_context_data(**kwargs)
        context['filter_form'] = ExportFilterForm()
        return context

    def post(self, *args, **kwargs):
        years = None
        filter_form = ExportFilterForm(self.request.POST)
        all_questionnaires = Questionnaire.objects.all()
        export_service = ExportToTextService(questionnaires=all_questionnaires)
        if filter_form.is_valid():
            years = filter_form.cleaned_data['year']
            countries = filter_form.cleaned_data['countries']
            regions = filter_form.cleaned_data['regions']
            themes = filter_form.cleaned_data['themes']

            query_params = {'year__in': years, 'region__countries__in': countries, 'region__in': regions}
            clean_query_params = filter_empty_values(query_params)

            all_questionnaires = all_questionnaires.filter(**clean_query_params)
            export_service = ExportToTextService(questionnaires=all_questionnaires, countries=countries, themes=themes)

        formatted_responses = export_service.get_formatted_responses()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s-%s.txt"' % (
        'data', '_'.join(years) or self.ALL_QUESTIONNAIRES)
        response.write("\r\n".join(formatted_responses))
        return response


class SpecificExportView(LoginRequiredMixin, TemplateView):
    template_name = "home/extract.html"

    def post(self, *args, **kwargs):
        country = Country.objects.get(id=kwargs['country_id'])
        questionnaire = Questionnaire.objects.filter(region__countries=country, status=Questionnaire.PUBLISHED).latest(
            'modified')
        version = kwargs.get('version_number', None)
        export_service = ExportToTextService([questionnaire], countries=[country], version=version)
        formatted_responses = export_service.get_formatted_responses()
        response = HttpResponse(content_type='text/csv')
        filename_parts = (questionnaire.name, questionnaire.year, country.name, version)
        response['Content-Disposition'] = 'attachment; filename="%s-%s-%s-%s.txt"' % filename_parts
        response.write("\r\n".join(formatted_responses))
        return response


class ExportSectionPDF(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        session_id = self.request.COOKIES['sessionid']
        file_name = 'eJRF_export_%s.pdf' % str(time.time())
        export_file = 'export/' + file_name

        # In case other get params recreate url string for printable param
        url_parts = list(urlparse.urlparse(self.request.META['HTTP_REFERER']))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update({'printable': '1'})
        url_parts[4] = urllib.urlencode(query)
        export_url = urlparse.urlunparse(url_parts)

        domain = str(self.request.META['HTTP_HOST']).split(':')[0]
        phantomjs_script = 'questionnaire/static/js/export-section.js'
        command = ["phantomjs", phantomjs_script, export_url, export_file, session_id, domain, "&> /dev/null &"]
        subprocess.Popen(command)
        return HttpResponse(json.dumps({'filename': file_name}))


class DownloadSectionPDF(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        filename = kwargs.get('filename', '')
        return_file = File(open('export/' + filename, 'r'))
        response = HttpResponse(return_file, mimetype='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        os.system("rm -rf export/%s" % filename)
        return response