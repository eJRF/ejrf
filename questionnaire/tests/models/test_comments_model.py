from django.contrib.auth.models import User

from questionnaire.models import Question, Country, NumericalAnswer, AnswerGroup, QuestionGroup, SubSection, Section, \
    Questionnaire
from questionnaire.models.comments import Comment
from questionnaire.tests.base_test import BaseTest


class CommentTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="Uganda Revision 2014", description="some description")
        self.question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123',
                                                answer_type='Text')
        self.country = Country.objects.create(name="Peru")
        self.tony = User.objects.create(username="Tony")
        self.montana = User.objects.create(username="Montana")
        self.section = Section.objects.create(title="Immunisation Coverage", order=1, questionnaire=self.questionnaire)
        self.sub_section = SubSection.objects.create(title="Immunisation Extra Coverage", order=1, section=self.section)
        self.grouped_question = QuestionGroup.objects.create(subsection=self.sub_section, order=1)
        self.answer = NumericalAnswer.objects.create(question=self.question, country=self.country, response=11.2)
        self.answer_group = AnswerGroup.objects.create(grouped_question=self.grouped_question, row=1)
        self.answer_group.answer.add(self.answer)

    def test_comment_fields(self):
        comment = Comment()
        fields = [str(item.attname) for item in comment._meta.fields]
        self.assertEqual(5, len(fields))
        for field in ['id', 'created', 'modified', 'text', 'user_id']:
            self.assertIn(field, fields)

    def test_comments_store(self):
        tony_comment = Comment.objects.create(user=self.tony, text="This is an absurd figure")
        montana_comment = Comment.objects.create(user=self.montana, text="This is an absurd figure")
        self.answer_group.comments.add(tony_comment)
        self.answer_group.comments.add(montana_comment)
        answer_comments = self.answer_group.comments.all()

        self.failUnless(tony_comment.id)
        self.failUnless(montana_comment.id)
        self.assertEqual(2, answer_comments.count())
        self.assertIn(montana_comment, answer_comments)
        self.assertIn(tony_comment, answer_comments)