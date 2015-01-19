from django.conf.urls import patterns, include, url
from questionnaire.urls import urlpatterns as questionnaire_urls
from questionnaire.api.urls import urlpatterns as questionnaire_api_urls

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
) + questionnaire_urls + questionnaire_api_urls
