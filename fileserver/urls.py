from django.urls import re_path, path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = format_suffix_patterns([

    re_path(r'^upload/?$', views.FileUploadList.as_view()),
    re_path(r'^upload/(?P<pk>[0-9]+)/?$', views.FileUploadDetail.as_view()),

    re_path(r'^lang/?$', views.LanguageList.as_view()),
    re_path(r'^lang/(?P<pk>[0-9]+)/?$', views.LanguageDetail.as_view()),
    re_path(r'^lang/count/?$', views.LanguageCounterList.as_view()),
    re_path(r'^lang/count/(?P<pk>[0-9]+)/?$', views.LanguageCounterDetail.as_view()),

    re_path(r'^doctype/?$', views.DoctypeList.as_view()),
    re_path(r'^doctype/(?P<pk>[0-9]+)/?$', views.DoctypeDetail.as_view()),
    re_path(r'^doctype/count/?$', views.DoctypeCounterList.as_view()),
    re_path(r'^doctype/count/(?P<pk>[0-9]+)/?$', views.DoctypeCounterDetail.as_view()),

    re_path(r'^conf-level/?$', views.ConfLevelList.as_view()),
    re_path(r'^conf-level/(?P<pk>[0-9]+)/?$', views.ConfLevelDetail.as_view()),
    re_path(r'^conf-level/count/?$', views.ConfLevelCounterList.as_view()),
    re_path(r'^conf-level/count/(?P<pk>[0-9]+)/?$', views.ConfLevelCounterDetail.as_view()),

])
