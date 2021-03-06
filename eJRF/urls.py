from django.conf.urls import patterns, include, url
from questionnaire.urls import urlpatterns as questionnaire_urls
from questionnaire.api.urls import urlpatterns as questionnaire_api_urls

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
) + questionnaire_urls + questionnaire_api_urls

urlpatterns += staticfiles_urlpatterns()

handler404 = 'questionnaire.views.errors.serve_404'
handler500 = 'questionnaire.views.errors.serve_500'