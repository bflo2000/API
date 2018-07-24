from django.conf.urls import url
from Amazon import views

urlpatterns = [
    url('amazon/$', views.amazon_variation_list.as_view()),
    url('amazon/(?P<sku>[0-9]+)/$', views.amazon_variation_detail.as_view()),
    url(r'amazon/upload_category_report', views.category_report_upload.as_view()),
    url(r'amazon/upload_variations', views.amazon_variation_upload.as_view()),
    url(r'amazon/category_sftp', views.category_report_sftp.as_view()),
    url(r'amazon/amazon_variation_sftp', views.amazon_variation_sftp.as_view())
]
