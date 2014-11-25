from questionnaire.models import Question
from questionnaire.models.themes import Theme
from questionnaire.tests.base_test import BaseTest
from questionnaire.utils.answer_type import AnswerTypes


class ThemeTest(BaseTest):
    def test_theme_fields(self):
        theme = Theme()
        fields = [str(item.attname) for item in theme._meta.fields]
        self.assertEqual(6, len(fields))
        for field in ['id', 'created', 'modified', 'name', 'description', 'region_id']:
            self.assertIn(field, fields)

    def test_theme_stores(self):
        theme = Theme.objects.create(name="Theme1", description="Our theme.")
        self.failUnless(theme.id)

    def test_theme_unicode(self):
        theme = Theme.objects.create(name="Theme1", description="Our theme.")
        self.assertEqual(str(theme), "Theme1".encode('utf8'))

    def test_theme_de_associates_its_questions(self):
        theme = Theme.objects.create(name="Theme1", description="Our theme.")
        beer_question = Question.objects.create(text="How many beers do you drink?", UID='BR01',
                                                answer_type=AnswerTypes.NUMBER, theme=theme)
        beer_question1 = Question.objects.create(text="When did you last drink beer?", UID='BR02',
                                                 answer_type=AnswerTypes.DATE, theme=theme)

        theme.de_associate_questions()
        self.assertEqual(0, theme.questions.all().count())
        self.assertNotIn(beer_question, theme.questions.all())
        self.assertNotIn(beer_question1, theme.questions.all())
