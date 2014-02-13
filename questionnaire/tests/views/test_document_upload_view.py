import os
from django.core.files import File
from django.core.urlresolvers import reverse_lazy
from django.test import Client
from mock import mock_open, patch
from questionnaire.forms.support_document_upload_form import SupportDocumentUploadForm

from questionnaire.tests.base_test import BaseTest
from questionnaire.models import Questionnaire, Country, SupportDocument


class UploadSupportDocumentTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user, self.country = self.create_user_with_no_permissions()
        self.login_user()
        self.filename = 'test_empty_file.pdf'
        self.uganda = Country.objects.create(name="Uganda")
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013)

        m = mock_open()
        with patch('__main__.open', m, create=True):
            with open(self.filename, 'w') as document:
                document.write("Some stuff")
            self.document = open(self.filename, 'rb')

    def test_get_upload_view(self):
        response = self.client.get('/questionnaire/documents/upload/')
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questionnaires/entry/upload.html', templates)
        self.assertEqual('Upload', response.context['button_label'])
        self.assertEqual(self.questionnaire, response.context['questionnaire'])
        self.assertIsInstance(response.context['upload_form'], SupportDocumentUploadForm)

    def test_upload_upload(self):
        data = {'questionnaire': self.questionnaire.id, 'country': self.uganda.id, 'path': self.document}
        response = self.client.post('/questionnaire/documents/upload/', data=data)
        _file = SupportDocument.objects.get(country=self.uganda, questionnaire=self.questionnaire)
        self.failUnless(_file)
        self.assertTrue(os.path.exists(_file.path.url))
        self.assertRedirects(response, '/questionnaire/documents/upload/', status_code=302)
        message = "File was uploaded successfully"
        self.assertIn(message, response.cookies['messages'].value)

    def test_user_does_not_exist_upload_upload(self):
        data = {'questionnaire': self.questionnaire.id, 'country': '', 'path': self.document}
        response = self.client.post('/questionnaire/documents/upload/', data=data)
        self.assertEqual(200, response.status_code)

    def test_download_attachment_view(self):
        uganda = Country.objects.create(name="Uganda")
        questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013)

        _document = SupportDocument.objects.create(path=File(self.document), country=uganda, questionnaire=questionnaire)
        url = '/questionnaire/entry/%s/documents/%s/download/' % (questionnaire.id, _document.id)
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_detach_file_attachment(self):
        _document = SupportDocument.objects.create(path=File(self.document), country=self.uganda,
                                                   questionnaire=self.questionnaire)
        self.failUnless(SupportDocument.objects.get(id=_document.id))
        self.assertTrue(os.path.exists(_document.path.url))

        url = '/questionnaire/document/%s/delete/' % _document.id
        response = self.client.get(url)
        self.assertRedirects(response, '/questionnaire/documents/upload/')

        self.assertRaises(SupportDocument.DoesNotExist, SupportDocument.objects.get, id=_document.id)
        self.assertFalse(os.path.exists(_document.path.url))

    def tear_down(self):
        os.system("rm -rf %s" % self.filename)
        os.system("rm -rf media/user_uploads/*")
