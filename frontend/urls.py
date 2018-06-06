from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url('app/$', TemplateView.as_view(template_name="index.html")),
]