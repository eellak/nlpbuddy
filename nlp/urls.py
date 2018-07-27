from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url, include
from django.contrib.sitemaps.views import sitemap
from django.urls import path

from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^about$', views.about, name='nlp.views.about'),
    url(r'^api/analyze$', views.analyze, name='nlp.views.analyze'),
]

