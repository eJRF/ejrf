from django.test import TestCase

from questionnaire.models import Country
import questionnaire.models
from questionnaire.models.questionnaires import CountryQuestionnaireSubmission


class CountryQuestionnaireSubmissionTest(TestCase):
    def setUp(self):
        self.questionnaire = questionnaire.models.Questionnaire.objects.create(name="JRF 2013 Core English",
                                                                               description="From dropbox as given by Rouslan")
        self.uganda = Country.objects.create(name='uganda')

    def test_answer_fields(self):
        country_questionnaire_submission = CountryQuestionnaireSubmission()
        fields = [str(item.attname) for item in country_questionnaire_submission._meta.fields]
        self.assertEqual(6, len(fields))
        for field in ['id', 'created', 'modified', 'country_id', 'questionnaire_id']:
            self.assertIn(field, fields)

    def test_save_submission(self):
        submission = CountryQuestionnaireSubmission.objects.create(country=self.uganda,
                                                                   questionnaire=self.questionnaire, version=1)
        self.assertEqual(submission.country, self.uganda)
        self.assertEqual(submission.questionnaire, self.questionnaire)