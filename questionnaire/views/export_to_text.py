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
from questionnaire.models import Questionnaire
from questionnaire.services.export_data_service import ExportToTextService


class ExportToTextView(LoginRequiredMixin, TemplateView):
    template_name = "home/extract.html"

    def get_context_data(self, **kwargs):
        context = super(ExportToTextView, self).get_context_data(**kwargs)
        context['questionnaires'] = Questionnaire.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(id=request.POST['questionnaire'])
        formatted_responses = ExportToTextService(questionnaire).get_formatted_responses()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s-%s.txt"'% (questionnaire.name, questionnaire.year)
        response.write("\r\n".join(formatted_responses))
        return response

class ExportSectionPDF(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        session_id = request.COOKIES['sessionid']
        file_name = 'eJRF_export_%s.pdf' % str(time.time())

        # In case other get params recreate url string for printable param
        url_parts = list(urlparse.urlparse(request.META['HTTP_REFERER']))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update({'printable': '1'})
        url_parts[4] = urllib.urlencode(query)
        export_url = urlparse.urlunparse(url_parts)

        url = (export_url)
        domain = str(request.META['HTTP_HOST']).split(':')[0]
        phantomjs_script = 'questionnaire/static/js/export-section.js'
        command = ["phantomjs", phantomjs_script, url, file_name, session_id, domain, "&> /dev/null &"]
        subprocess.Popen(command)
        return HttpResponse(json.dumps({'filename': file_name}))


class DownloadSectionPDF(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        filename = kwargs.get('filename', None)
        return_file = File(open(filename, 'r'))
        response = HttpResponse(return_file, mimetype='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        os.system("rm -rf %s" % filename)
        return response
