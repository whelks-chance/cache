"""cache URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.views.static import serve
from django.conf.urls import url, include
from django.contrib import admin

from django.conf import settings
# from django.conf.urls.static import static
from cachevis import views as cachevis_views
from housing_portal import views, survey_api

urlpatterns = [
    url(r'^$', views.eg1, name='home'),

    url(r'^admin/', admin.site.urls),

    url(r'^base/', views.base),
    url(r'^example/', views.example),

    url(r'^search/', views.search, name='search'),
    url(r'^search_results/', views.search_results, name='search_results'),

    url(r'^survey_metadata/(?P<survey_id>\S+)', survey_api.survey_metadata, name='survey_metadata'),
    url(r'^survey_dc_info/(?P<survey_id>\S+)', survey_api.survey_dc_info, name='survey_dc_info'),
    url(r'^survey_questions/(?P<survey_id>\S+)', survey_api.survey_questions, name='survey_questions'),

    url(r'^survey_single_question/(?P<question_id>\S+)',
        survey_api.survey_single_question, name='survey_single_question'),
    url(r'^survey_question_results/(?P<question_id>\S+)',
        survey_api.survey_question_results, name='survey_question_results'),
    url(r'^response_table/(?P<question_id>\S+)',
        survey_api.response_table, name='response_table'),

    url(r'^survey_detail/(?P<survey_id>\S+)', views.survey_detail, name='survey_detail'),
    url(r'^survey_question/(?P<question_id>\S+)', views.survey_question, name='survey_question'),

    url(r'^test/', views.test, name='test'),
    url(r'^map_test/', views.map_test, name='map_test'),

    url(r'^eg1/', views.eg1, name='eg1'),

    url(r'cachevis/test', cachevis_views.test, name='cachevis_test'),
    url(r'cachevis/bank_share', cachevis_views.bank_share, name='bank_share'),

    #   Be careful not to let nginx forward this to the actual ckan server
    url(r'^local_ckan/search', views.ckan_search, name='ckan_search'),
    url(r'^local_ckan/resource', views.ckan_resource, name='ckan_resource'),
    url(r'^local_ckan/dataset', views.ckan_dataset, name='ckan_dataset'),

    url(regex=r'^%s(?P<path>.*)$' % settings.STATIC_URL[1:],
        view=serve,
        kwargs={
            'document_root': settings.STATIC_ROOT,
            'show_indexes': True
        }
    ),
    url(r'^wiki/notifications/', include('django_nyt.urls')),
    url(r'^wiki/', include('wiki.urls'))

]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
