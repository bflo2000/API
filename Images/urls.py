from django.conf.urls import url
from snippets import views

urlpatterns = [
    url(r'^images/$', views.image_list),
    url(r'^images/(?P<pk>[0-9]+)/$', views.image_detail),
]