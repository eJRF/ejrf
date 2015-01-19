from django.conf.urls import patterns, url

from questionnaire.api.v1.questions import QuestionAPIView


urlpatterns = patterns('',
                       url(r'^api/v1/questions/$', QuestionAPIView.as_view()),
)
