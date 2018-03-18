from django.conf.urls import url
from Amazon import views

urlpatterns = [
    url('amazon/$', views.amazon_variation_list.as_view()),
    url('amazon/(?P<pk>[0-9]+)/$', views.amazon_variation_detail.as_view()),
    url(r'amazon/upload', views.amazon_variation_upload.as_view())
]