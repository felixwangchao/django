from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index, name = 'index'),
    url(r'^success/$', views.success, name = 'success'),
    url(r'^[\s\S]+/$',views.toUpload, name = 'toUpload'),
]
