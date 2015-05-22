"""vld_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
# pylint: disable=invalid-name,line-too-long,bad-continuation
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

import ingredient.urls
import persons.urls
import meals.urls

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^ingredient/', include(ingredient.urls, namespace='ingredient')),
    url(r'^persons/', include(persons.urls, namespace='persons')),
    url(r'^meals/', include(meals.urls, namespace='meals')),
    url(r'^admin/', include(admin.site.urls)),
]  # yapf: disable

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )  # yapf: disable
    urlpatterns += patterns(
        "",
        url(r"^media/(?P<path>.*)$", "django.views.static.serve", {"document_root": settings.MEDIA_ROOT}),
        url(r"^static/(?P<path>.*)$", "django.views.static.serve", {"document_root": settings.STATIC_ROOT}),
    )  # yapf: disable
    urlpatterns += staticfiles_urlpatterns()
