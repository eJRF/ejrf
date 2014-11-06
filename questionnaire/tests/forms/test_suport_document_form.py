import os

from mock import mock_open, patch
from django.core.files.uploadedfile import SimpleUploadedFile

from eJRF.settings import ACCEPTED_EXTENSIONS
from questionnaire.forms.support_documents import SupportDocumentUploadForm
from questionnaire.models import Questionnaire, Country
from questionnaire.tests.base_test import BaseTest


class SupportDocumentTest(BaseTest):
    def setUp(self):
        self.filename = 'empty_file'
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013)
        self.uganda = Country.objects.create(name="Uganda")

    def tearDown(self):
        os.system("rm -rf %s" % self.filename)

    def test_should_know_fields(self):
        upload_form = SupportDocumentUploadForm()

        fields = ['path']

        [self.assertIn(field, upload_form.fields) for field in fields]

    def test_empty_file(self):
        data_file = {'path': SimpleUploadedFile(self.filename, open(self.filename, 'a').close())}
        initial = {'questionnaire': self.questionnaire.id, 'country': self.uganda.id}
        upload_document_form = SupportDocumentUploadForm(data={}, files=data_file, initial=initial, )
        self.assertFalse(upload_document_form.is_valid())
        self.assertIn('The submitted file is empty.', upload_document_form.errors['path'])

    def test_not_allowed_extension(self):
        self.filename = 'executable_file.exe'
        m = mock_open()
        with patch('__main__.open', m, create=True):
            with open(self.filename, 'w') as document:
                document.write("Some stuff")
            document = open(self.filename, 'rb')
            file_data = {'path': SimpleUploadedFile(self.filename, document.read())}
            data = {'questionnaire': self.questionnaire.id, 'country': self.uganda.id}
            upload_document_form = SupportDocumentUploadForm(data=data, files=file_data)
            self.assertFalse(upload_document_form.is_valid())
            error_message = ".exe file type is not an allowed, Please upload %s files only" % ', '.join(
                ACCEPTED_EXTENSIONS)
            self.assertIn(error_message, upload_document_form.errors['path'])

    def test_allowed_extension(self):
        self.filename = 'non_executable_file.pdf'
        m = mock_open()
        with patch('__main__.open', m, create=True):
            with open(self.filename, 'w') as document:
                document.write("Some stuff")
            document = open(self.filename, 'rb')
            file_data = {'path': SimpleUploadedFile(self.filename, document.read())}
            data = {'questionnaire': self.questionnaire.id, 'country': self.uganda.id}
            upload_document_form = SupportDocumentUploadForm(data=data, files=file_data)
            self.assertTrue(upload_document_form.is_valid())