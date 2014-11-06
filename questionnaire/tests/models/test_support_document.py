from questionnaire.models import Questionnaire, Country
from questionnaire.models.support_document import SupportDocument
from questionnaire.tests.base_test import BaseTest


class FileAnswerTest(BaseTest):
    def test_file_answer_fields(self):
        _file = SupportDocument()
        fields = [str(item.attname) for item in _file._meta.fields]
        self.assertEqual(6, len(fields))
        for field in ['id', 'created', 'modified', 'country_id', 'path', 'questionnaire_id']:
            self.assertIn(field, fields)

    def test_file_answer_field_store(self):
        questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English")
        country = Country.objects.create(name="Uganda")
        pdf_file_name = "/docs/user_files/survey2013.pdf"
        _file = SupportDocument.objects.create(questionnaire=questionnaire, country=country, path=pdf_file_name)
        self.failUnless(_file.id)
        self.assertEqual(pdf_file_name, _file.path)