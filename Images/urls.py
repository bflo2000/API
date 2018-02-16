from django.conf.urls import url
from Images import views

urlpatterns = [
    url('images/$', views.image_list.as_view()),
    url('images/(?P<pk>[0-9]+)/$', views.image_detail.as_view()),
]