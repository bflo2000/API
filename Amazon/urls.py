from django.conf.urls import url
from Amazon import views

urlpatterns = [
    url('amazon/$', views.amazon_variation_list.as_view()),
    url('amazon/(?P<sku>[0-9]+)/$', views.amazon_variation_detail.as_view()),
    url(r'amazon/upload', views.amazon_variation_upload.as_view()),
    url(r'amazon/sftp', views.amazon_variation_sftp.as_view()),
    url(r'amazon/size_verify', views.amazon_variation_size_verify.as_view()),
]