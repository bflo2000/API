from django.conf.urls import url
from Images import views

urlpatterns = [
    url('images/$', views.ImageList.as_view()),
    url('images/(?P<pk>[0-9]+)/$', views.ImageDetail.as_view()),
    url(r'images/upload', views.ImageUpload.as_view()),
    url(r'images/sftp', views.ImagesSFTP.as_view()),
]