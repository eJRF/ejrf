from django.conf.urls import patterns, url
from questionnaire.api.v1.question_option import QuestionOptionAPIView

from questionnaire.api.v1.questions import QuestionAPIView
from questionnaire.api.v1.themes import ThemeAPIView
from questionnaire.api.v1.grid import GridAPIView

urlpatterns = patterns('',
   url(r'^api/v1/questions/$', QuestionAPIView.as_view()),
   url(r'^api/v1/themes/$', ThemeAPIView.as_view()),
   url(r'^api/v1/question/(?P<question_id>\d+)/options/$', QuestionOptionAPIView.as_view()),
   url(r'^api/v1/subsection/(?P<subsection_id>\d+)/grid/(?P<grid_id>\d+)/$', GridAPIView.as_view()),
)