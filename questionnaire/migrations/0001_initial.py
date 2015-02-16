# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'questionnaire_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='user_profile', unique=True, to=orm['auth.User'])),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questionnaire.Region'], null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questionnaire.Country'], null=True, blank=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questionnaire.Organization'], null=True, blank=True)),
        ))
        db.send_create_signal('questionnaire', ['UserProfile'])

        # Adding model 'Question'
        db.create_table(u'questionnaire_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('export_label', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('instructions', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('UID', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('answer_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('answer_sub_type', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(related_name='questions', null=True, to=orm['questionnaire.Region'])),
            ('theme', self.gf('django.db.models.fields.related.ForeignKey')(related_name='questions', null=True, to=orm['questionnaire.Theme'])),
            ('is_primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='child', null=True, to=orm['questionnaire.Question'])),
        ))
        db.send_create_signal('questionnaire', ['Question'])

        # Adding model 'QuestionOption'
        db.create_table(u'questionnaire_questionoption', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='options', to=orm['questionnaire.Question'])),
            ('instructions', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('UID', self.gf('django.db.models.fields.CharField')(max_length=6, unique=True, null=True)),
        ))
        db.send_create_signal('questionnaire', ['QuestionOption'])

        # Adding model 'Answer'
        db.create_table(u'questionnaire_answer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', null=True, to=orm['questionnaire.Question'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questionnaire.Country'], null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='Draft', max_length=15)),
            ('version', self.gf('django.db.models.fields.IntegerField')(default=1, null=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('questionnaire', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', null=True, to=orm['questionnaire.Questionnaire'])),
        ))
        db.send_create_signal('questionnaire', ['Answer'])

        # Adding model 'NumericalAnswer'
        db.create_table(u'questionnaire_numericalanswer', (
            (u'answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['questionnaire.Answer'], unique=True, primary_key=True)),
            ('response', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
        ))
        db.send_create_signal('questionnaire', ['NumericalAnswer'])

        # Adding model 'TextAnswer'
        db.create_table(u'questionnaire_textanswer', (
            (u'answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['questionnaire.Answer'], unique=True, primary_key=True)),
            ('response', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('questionnaire', ['TextAnswer'])

        # Adding model 'DateAnswer'
        db.create_table(u'questionnaire_dateanswer', (
            (u'answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['questionnaire.Answer'], unique=True, primary_key=True)),
            ('response', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
        ))
        db.send_create_signal('questionnaire', ['DateAnswer'])

        # Adding model 'MultiChoiceAnswer'
        db.create_table(u'questionnaire_multichoiceanswer', (
            (u'answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['questionnaire.Answer'], unique=True, primary_key=True)),
            ('response', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answer', null=True, to=orm['questionnaire.QuestionOption'])),
        ))
        db.send_create_signal('questionnaire', ['MultiChoiceAnswer'])

        # Adding model 'MultipleResponseAnswer'
        db.create_table(u'questionnaire_multipleresponseanswer', (
            (u'answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['questionnaire.Answer'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('questionnaire', ['MultipleResponseAnswer'])

        # Adding M2M table for field response on 'MultipleResponseAnswer'
        db.create_table(u'questionnaire_multipleresponseanswer_response', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('multipleresponseanswer', models.ForeignKey(orm['questionnaire.multipleresponseanswer'], null=False)),
            ('questionoption', models.ForeignKey(orm['questionnaire.questionoption'], null=False))
        ))
        db.create_unique(u'questionnaire_multipleresponseanswer_response', ['multipleresponseanswer_id', 'questionoption_id'])

        # Adding model 'Comment'
        db.create_table(u'questionnaire_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('questionnaire', ['Comment'])

        # Adding M2M table for field answer_group on 'Comment'
        db.create_table(u'questionnaire_comment_answer_group', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('comment', models.ForeignKey(orm['questionnaire.comment'], null=False)),
            ('answergroup', models.ForeignKey(orm['questionnaire.answergroup'], null=False))
        ))
        db.create_unique(u'questionnaire_comment_answer_group', ['comment_id', 'answergroup_id'])

        # Adding model 'AnswerGroup'
        db.create_table(u'questionnaire_answergroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('grouped_question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answer_groups', null=True, to=orm['questionnaire.QuestionGroup'])),
            ('row', self.gf('django.db.models.fields.CharField')(max_length=6)),
        ))
        db.send_create_signal('questionnaire', ['AnswerGroup'])

        # Adding M2M table for field answer on 'AnswerGroup'
        db.create_table(u'questionnaire_answergroup_answer', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('answergroup', models.ForeignKey(orm['questionnaire.answergroup'], null=False)),
            ('answer', models.ForeignKey(orm['questionnaire.answer'], null=False))
        ))
        db.create_unique(u'questionnaire_answergroup_answer', ['answergroup_id', 'answer_id'])

        # Adding model 'QuestionGroupOrder'
        db.create_table(u'questionnaire_questiongrouporder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orders', to=orm['questionnaire.Question'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('question_group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orders', null=True, to=orm['questionnaire.QuestionGroup'])),
        ))
        db.send_create_signal('questionnaire', ['QuestionGroupOrder'])

        # Adding unique constraint on 'QuestionGroupOrder', fields ['order', 'question_group', 'question']
        db.create_unique(u'questionnaire_questiongrouporder', ['order', 'question_group_id', 'question_id'])

        # Adding model 'QuestionGroup'
        db.create_table(u'questionnaire_questiongroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('subsection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='question_group', to=orm['questionnaire.SubSection'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('instructions', self.gf('django.db.models.fields.TextField')(null=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sub_group', null=True, to=orm['questionnaire.QuestionGroup'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('allow_multiples', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('grid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('display_all', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hybrid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_core', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('questionnaire', ['QuestionGroup'])

        # Adding M2M table for field question on 'QuestionGroup'
        db.create_table(u'questionnaire_questiongroup_question', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('questiongroup', models.ForeignKey(orm['questionnaire.questiongroup'], null=False)),
            ('question', models.ForeignKey(orm['questionnaire.question'], null=False))
        ))
        db.create_unique(u'questionnaire_questiongroup_question', ['questiongroup_id', 'question_id'])

        # Adding model 'Organization'
        db.create_table(u'questionnaire_organization', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
        ))
        db.send_create_signal('questionnaire', ['Organization'])

        # Adding model 'Region'
        db.create_table(u'questionnaire_region', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(related_name='regions', null=True, to=orm['questionnaire.Organization'])),
        ))
        db.send_create_signal('questionnaire', ['Region'])

        # Adding model 'Country'
        db.create_table(u'questionnaire_country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=5, null=True)),
        ))
        db.send_create_signal('questionnaire', ['Country'])

        # Adding M2M table for field regions on 'Country'
        db.create_table(u'questionnaire_country_regions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('country', models.ForeignKey(orm['questionnaire.country'], null=False)),
            ('region', models.ForeignKey(orm['questionnaire.region'], null=False))
        ))
        db.create_unique(u'questionnaire_country_regions', ['country_id', 'region_id'])

        # Adding model 'Questionnaire'
        db.create_table(u'questionnaire_questionnaire', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('year', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('status', self.gf('model_utils.fields.StatusField')(default='draft', max_length=100, no_check_for_status=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='questionnaire', null=True, to=orm['questionnaire.Region'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['questionnaire.Questionnaire'])),
        ))
        db.send_create_signal('questionnaire', ['Questionnaire'])

        # Adding model 'CountryQuestionnaireSubmission'
        db.create_table(u'questionnaire_countryquestionnairesubmission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='submissions', to=orm['questionnaire.Country'])),
            ('questionnaire', self.gf('django.db.models.fields.related.ForeignKey')(related_name='submissions', to=orm['questionnaire.Questionnaire'])),
            ('version', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('questionnaire', ['CountryQuestionnaireSubmission'])

        # Adding model 'Section'
        db.create_table(u'questionnaire_section', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('questionnaire', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sections', to=orm['questionnaire.Questionnaire'])),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sections', null=True, to=orm['questionnaire.Region'])),
            ('is_core', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('questionnaire', ['Section'])

        # Adding model 'SubSection'
        db.create_table(u'questionnaire_subsection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sub_sections', to=orm['questionnaire.Section'])),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sub_sections', null=True, to=orm['questionnaire.Region'])),
            ('is_core', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('questionnaire', ['SubSection'])

        # Adding model 'SkipRule'
        db.create_table(u'questionnaire_skiprule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('root_question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='root_skip_rules', to=orm['questionnaire.Question'])),
            ('response', self.gf('django.db.models.fields.related.ForeignKey')(related_name='skip_rules', to=orm['questionnaire.QuestionOption'])),
            ('subsection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='skip_rules', to=orm['questionnaire.SubSection'])),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='skip_rules', null=True, to=orm['questionnaire.Region'])),
        ))
        db.send_create_signal('questionnaire', ['SkipRule'])

        # Adding model 'SkipQuestion'
        db.create_table(u'questionnaire_skipquestion', (
            (u'skiprule_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['questionnaire.SkipRule'], unique=True, primary_key=True)),
            ('skip_question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='skip_rules', to=orm['questionnaire.Question'])),
        ))
        db.send_create_signal('questionnaire', ['SkipQuestion'])

        # Adding model 'SkipSubsection'
        db.create_table(u'questionnaire_skipsubsection', (
            (u'skiprule_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['questionnaire.SkipRule'], unique=True, primary_key=True)),
            ('skip_subsection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questionnaire.SubSection'])),
        ))
        db.send_create_signal('questionnaire', ['SkipSubsection'])

        # Adding model 'SupportDocument'
        db.create_table(u'questionnaire_supportdocument', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('questionnaire', self.gf('django.db.models.fields.related.ForeignKey')(related_name='support_documents', to=orm['questionnaire.Questionnaire'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questionnaire.Country'])),
            ('path', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('questionnaire', ['SupportDocument'])

        # Adding model 'Theme'
        db.create_table(u'questionnaire_theme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=500, null=True, blank=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='themes', null=True, to=orm['questionnaire.Region'])),
        ))
        db.send_create_signal('questionnaire', ['Theme'])


    def backwards(self, orm):
        # Removing unique constraint on 'QuestionGroupOrder', fields ['order', 'question_group', 'question']
        db.delete_unique(u'questionnaire_questiongrouporder', ['order', 'question_group_id', 'question_id'])

        # Deleting model 'UserProfile'
        db.delete_table(u'questionnaire_userprofile')

        # Deleting model 'Question'
        db.delete_table(u'questionnaire_question')

        # Deleting model 'QuestionOption'
        db.delete_table(u'questionnaire_questionoption')

        # Deleting model 'Answer'
        db.delete_table(u'questionnaire_answer')

        # Deleting model 'NumericalAnswer'
        db.delete_table(u'questionnaire_numericalanswer')

        # Deleting model 'TextAnswer'
        db.delete_table(u'questionnaire_textanswer')

        # Deleting model 'DateAnswer'
        db.delete_table(u'questionnaire_dateanswer')

        # Deleting model 'MultiChoiceAnswer'
        db.delete_table(u'questionnaire_multichoiceanswer')

        # Deleting model 'MultipleResponseAnswer'
        db.delete_table(u'questionnaire_multipleresponseanswer')

        # Removing M2M table for field response on 'MultipleResponseAnswer'
        db.delete_table('questionnaire_multipleresponseanswer_response')

        # Deleting model 'Comment'
        db.delete_table(u'questionnaire_comment')

        # Removing M2M table for field answer_group on 'Comment'
        db.delete_table('questionnaire_comment_answer_group')

        # Deleting model 'AnswerGroup'
        db.delete_table(u'questionnaire_answergroup')

        # Removing M2M table for field answer on 'AnswerGroup'
        db.delete_table('questionnaire_answergroup_answer')

        # Deleting model 'QuestionGroupOrder'
        db.delete_table(u'questionnaire_questiongrouporder')

        # Deleting model 'QuestionGroup'
        db.delete_table(u'questionnaire_questiongroup')

        # Removing M2M table for field question on 'QuestionGroup'
        db.delete_table('questionnaire_questiongroup_question')

        # Deleting model 'Organization'
        db.delete_table(u'questionnaire_organization')

        # Deleting model 'Region'
        db.delete_table(u'questionnaire_region')

        # Deleting model 'Country'
        db.delete_table(u'questionnaire_country')

        # Removing M2M table for field regions on 'Country'
        db.delete_table('questionnaire_country_regions')

        # Deleting model 'Questionnaire'
        db.delete_table(u'questionnaire_questionnaire')

        # Deleting model 'CountryQuestionnaireSubmission'
        db.delete_table(u'questionnaire_countryquestionnairesubmission')

        # Deleting model 'Section'
        db.delete_table(u'questionnaire_section')

        # Deleting model 'SubSection'
        db.delete_table(u'questionnaire_subsection')

        # Deleting model 'SkipRule'
        db.delete_table(u'questionnaire_skiprule')

        # Deleting model 'SkipQuestion'
        db.delete_table(u'questionnaire_skipquestion')

        # Deleting model 'SkipSubsection'
        db.delete_table(u'questionnaire_skipsubsection')

        # Deleting model 'SupportDocument'
        db.delete_table(u'questionnaire_supportdocument')

        # Deleting model 'Theme'
        db.delete_table(u'questionnaire_theme')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'questionnaire.answer': {
            'Meta': {'object_name': 'Answer'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.Country']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'null': 'True', 'to': "orm['questionnaire.Question']"}),
            'questionnaire': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'null': 'True', 'to': "orm['questionnaire.Questionnaire']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Draft'", 'max_length': '15'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True'})
        },
        'questionnaire.answergroup': {
            'Meta': {'object_name': 'AnswerGroup'},
            'answer': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'answergroup'", 'null': 'True', 'to': "orm['questionnaire.Answer']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'grouped_question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answer_groups'", 'null': 'True', 'to': "orm['questionnaire.QuestionGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'row': ('django.db.models.fields.CharField', [], {'max_length': '6'})
        },
        'questionnaire.comment': {
            'Meta': {'object_name': 'Comment'},
            'answer_group': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'comments'", 'symmetrical': 'False', 'to': "orm['questionnaire.AnswerGroup']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'questionnaire.country': {
            'Meta': {'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'regions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'countries'", 'null': 'True', 'to': "orm['questionnaire.Region']"})
        },
        'questionnaire.countryquestionnairesubmission': {
            'Meta': {'object_name': 'CountryQuestionnaireSubmission'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'submissions'", 'to': "orm['questionnaire.Country']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'questionnaire': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'submissions'", 'to': "orm['questionnaire.Questionnaire']"}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'questionnaire.dateanswer': {
            'Meta': {'object_name': 'DateAnswer', '_ormbases': ['questionnaire.Answer']},
            u'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['questionnaire.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'response': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'})
        },
        'questionnaire.multichoiceanswer': {
            'Meta': {'object_name': 'MultiChoiceAnswer', '_ormbases': ['questionnaire.Answer']},
            u'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['questionnaire.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'response': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answer'", 'null': 'True', 'to': "orm['questionnaire.QuestionOption']"})
        },
        'questionnaire.multipleresponseanswer': {
            'Meta': {'object_name': 'MultipleResponseAnswer', '_ormbases': ['questionnaire.Answer']},
            u'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['questionnaire.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'response': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'answers'", 'null': 'True', 'to': "orm['questionnaire.QuestionOption']"})
        },
        'questionnaire.numericalanswer': {
            'Meta': {'object_name': 'NumericalAnswer', '_ormbases': ['questionnaire.Answer']},
            u'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['questionnaire.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'response': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'})
        },
        'questionnaire.organization': {
            'Meta': {'object_name': 'Organization'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        'questionnaire.question': {
            'Meta': {'object_name': 'Question'},
            'UID': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'answer_sub_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'answer_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'export_label': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child'", 'null': 'True', 'to': "orm['questionnaire.Question']"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'null': 'True', 'to': "orm['questionnaire.Region']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'null': 'True', 'to': "orm['questionnaire.Theme']"})
        },
        'questionnaire.questiongroup': {
            'Meta': {'ordering': "('order',)", 'object_name': 'QuestionGroup'},
            'allow_multiples': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_all': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'grid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hybrid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'is_core': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sub_group'", 'null': 'True', 'to': "orm['questionnaire.QuestionGroup']"}),
            'question': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'question_group'", 'symmetrical': 'False', 'to': "orm['questionnaire.Question']"}),
            'subsection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'question_group'", 'to': "orm['questionnaire.SubSection']"})
        },
        'questionnaire.questiongrouporder': {
            'Meta': {'ordering': "('order',)", 'unique_together': "(('order', 'question_group', 'question'),)", 'object_name': 'QuestionGroupOrder'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['questionnaire.Question']"}),
            'question_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'null': 'True', 'to': "orm['questionnaire.QuestionGroup']"})
        },
        'questionnaire.questionnaire': {
            'Meta': {'object_name': 'Questionnaire'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['questionnaire.Questionnaire']"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'questionnaire'", 'null': 'True', 'to': "orm['questionnaire.Region']"}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'max_length': '100', u'no_check_for_status': 'True'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'questionnaire.questionoption': {
            'Meta': {'ordering': "('modified',)", 'object_name': 'QuestionOption'},
            'UID': ('django.db.models.fields.CharField', [], {'max_length': '6', 'unique': 'True', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'options'", 'to': "orm['questionnaire.Question']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'questionnaire.region': {
            'Meta': {'object_name': 'Region'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'regions'", 'null': 'True', 'to': "orm['questionnaire.Organization']"})
        },
        'questionnaire.section': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Section'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_core': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'questionnaire': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sections'", 'to': "orm['questionnaire.Questionnaire']"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sections'", 'null': 'True', 'to': "orm['questionnaire.Region']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'questionnaire.skipquestion': {
            'Meta': {'object_name': 'SkipQuestion', '_ormbases': ['questionnaire.SkipRule']},
            'skip_question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'skip_rules'", 'to': "orm['questionnaire.Question']"}),
            u'skiprule_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['questionnaire.SkipRule']", 'unique': 'True', 'primary_key': 'True'})
        },
        'questionnaire.skiprule': {
            'Meta': {'object_name': 'SkipRule'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'skip_rules'", 'null': 'True', 'to': "orm['questionnaire.Region']"}),
            'response': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'skip_rules'", 'to': "orm['questionnaire.QuestionOption']"}),
            'root_question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'root_skip_rules'", 'to': "orm['questionnaire.Question']"}),
            'subsection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'skip_rules'", 'to': "orm['questionnaire.SubSection']"})
        },
        'questionnaire.skipsubsection': {
            'Meta': {'object_name': 'SkipSubsection', '_ormbases': ['questionnaire.SkipRule']},
            'skip_subsection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.SubSection']"}),
            u'skiprule_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['questionnaire.SkipRule']", 'unique': 'True', 'primary_key': 'True'})
        },
        'questionnaire.subsection': {
            'Meta': {'ordering': "('order',)", 'object_name': 'SubSection'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_core': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sub_sections'", 'null': 'True', 'to': "orm['questionnaire.Region']"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sub_sections'", 'to': "orm['questionnaire.Section']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        'questionnaire.supportdocument': {
            'Meta': {'object_name': 'SupportDocument'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.Country']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'path': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'questionnaire': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'support_documents'", 'to': "orm['questionnaire.Questionnaire']"})
        },
        'questionnaire.textanswer': {
            'Meta': {'object_name': 'TextAnswer', '_ormbases': ['questionnaire.Answer']},
            u'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['questionnaire.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'response': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        'questionnaire.theme': {
            'Meta': {'object_name': 'Theme'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'themes'", 'null': 'True', 'to': "orm['questionnaire.Region']"})
        },
        'questionnaire.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.Country']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.Organization']", 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.Region']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'user_profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['questionnaire']