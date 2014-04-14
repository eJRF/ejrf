import os
from urllib import quote
from django.core.files import File
from django.core.urlresolvers import reverse
from django.test import Client
from mock import mock_open, patch
from questionnaire.forms.support_documents import SupportDocumentUploadForm

from questionnaire.tests.base_test import BaseTest
from questionnaire.models import Questionnaire, Country, SupportDocument, Section


class UploadSupportDocumentTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user = self.create_user(group=self.DATA_SUMBITTER, country="Uganda", region="AFRO")

        self.assign('can_submit_responses', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.uganda = self.user.user_profile.country
        self.client.login(username='user', password='pass')
        self.filename = 'test_empty_file.pdf'
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013)
        self.section1 = Section.objects.create(name="section1", order=1, questionnaire=self.questionnaire)
        self.section2 = Section.objects.create(name="section2", order=2, questionnaire=self.questionnaire)
        self.kenyan_filename = "hehe.pdf"

        m = mock_open()
        with patch('__main__.open', m, create=True):
            with open(self.filename, 'w') as document:
                document.write("Some stuff")
            self.document = open(self.filename, 'rb')

        self.url = '/questionnaire/entry/%d/documents/upload/'%self.questionnaire.id

    def test_get_upload_view(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questionnaires/entry/upload.html', templates)
        self.assertEqual('Upload', response.context['button_label'])
        self.assertEqual(self.questionnaire, response.context['questionnaire'])
        ordered_sections = response.context['ordered_sections']
        self.assertEqual(2, ordered_sections.count())
        self.assertEqual(self.section1, ordered_sections[0])
        self.assertEqual(self.section2, ordered_sections[1])
        self.assertIsInstance(response.context['upload_form'], SupportDocumentUploadForm)
        self.assertIsNotNone(response.context['preview'])
        self.assertEqual(reverse("new_section_page", args=(self.questionnaire.id,)), response.context['new_section_action'])
        self.assertEqual(reverse('upload_document', args=(self.questionnaire.id,)), response.context['action'])

    def test_upload_view_has_all_document_for_questionnaire(self):
        document_in = SupportDocument.objects.create(path=File(self.document), country=self.uganda,
                                                   questionnaire=self.questionnaire)
        questionnaire_2 = Questionnaire.objects.create(name="haha", year=2013)
        document_not_in = SupportDocument.objects.create(path=File(self.document), country=self.uganda,
                                                   questionnaire=questionnaire_2)

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        documents = response.context['documents']
        self.assertEqual(1, documents.count())
        self.assertIn(document_in, documents)
        self.assertNotIn(document_not_in, documents)

    def test_upload_upload(self):
        data = {'questionnaire': self.questionnaire.id, 'country': self.uganda.id, 'path': self.document}
        response = self.client.post(self.url, data=data)
        _file = SupportDocument.objects.get(country=self.uganda, questionnaire=self.questionnaire)
        self.failUnless(_file)
        self.assertTrue(os.path.exists(_file.path.url))
        self.assertRedirects(response, self.url, status_code=302)
        message = "File was uploaded successfully"
        self.assertIn(message, response.cookies['messages'].value)

    def test_user_does_not_exist_upload_upload(self):
        data = {'questionnaire': self.questionnaire.id, 'country': '', 'path': self.document}
        response = self.client.post(self.url, data=data)
        self.assertEqual(200, response.status_code)

    def test_download_attachment_view(self):
        uganda = Country.objects.create(name="Uganda")
        questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013)

        _document = SupportDocument.objects.create(path=File(self.document), country=uganda, questionnaire=questionnaire)
        url = '/questionnaire/entry/%s/documents/%s/download/' % (questionnaire.id, _document.id)
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_assert_login_required(self):
        url = '/questionnaire/entry/1/documents/2/download/'
        self.assert_login_required(url)

    def test_detach_file_attachment(self):
        _document = SupportDocument.objects.create(path=File(self.document), country=self.uganda,
                                                   questionnaire=self.questionnaire)
        self.failUnless(SupportDocument.objects.get(id=_document.id))
        self.assertTrue(os.path.exists(_document.path.url))

        url = '/questionnaire/document/%s/delete/' % _document.id
        response = self.client.post(url)
        self.assertRedirects(response, self.url)

        self.assertRaises(SupportDocument.DoesNotExist, SupportDocument.objects.get, id=_document.id)
        self.assertFalse(os.path.exists(_document.path.url))

    def test_permission_required_for_delete_document(self):
        _document = SupportDocument.objects.create(path=File(self.document), country=self.uganda,
                                                   questionnaire=self.questionnaire)
        url = '/questionnaire/document/%s/delete/' % _document.id
        self.assert_permission_required(url)

        user_not_in_same_country, country, region = self.create_user_with_no_permissions(username="asian_chic",
                                                                                        country_name="China",
                                                                                        region_name="ASEAN")
        self.assign('can_edit_questionnaire', user_not_in_same_country)

        self.client.logout()
        self.client.login(username='asian_chic', password='pass')
        response = self.client.post(url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % quote(url))

    def test_file_uploaded_by_user_cannot_be_seen_by_other_user(self):
        m = mock_open()
        with patch('__main__.open', m, create=True):
            with open(self.kenyan_filename, 'w') as document:
                document.write("Some stuff")
            kenya_document = open(self.kenyan_filename, 'rb')
        kenya = Country.objects.create(name="Kenya")
        kenya_document = SupportDocument.objects.create(path=File(kenya_document), country=kenya, questionnaire=self.questionnaire)
        uganda_document = SupportDocument.objects.create(path=File(self.document), country=self.uganda, questionnaire=self.questionnaire)

        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)
        self.assertNotIn(kenya_document, response.context['documents'])
        self.assertIn(uganda_document, response.context['documents'])

    def test_permission_reguired(self):
        self.assert_permission_required(self.url)

    def tearDown(self):
        os.system("rm -rf %s" % self.filename)
        os.system("rm -rf %s" % self.kenyan_filename)
        os.system("rm -rf media/user_uploads/*")