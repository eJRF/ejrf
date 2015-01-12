# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Questionnaire.parent'
        db.add_column(u'questionnaire_questionnaire', 'parent',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['questionnaire.Questionnaire']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Questionnaire.parent'
        db.delete_column(u'questionnaire_questionnaire', 'parent_id')


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
            'old_response': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
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
            'old_response': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '2', 'blank': 'True'}),
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