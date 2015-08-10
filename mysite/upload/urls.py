from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index, name = 'index'),
    url(r'^login/$', views.my_view, name = 'my_view'),
    url(r'^logout/$', views.logout_view, name = 'logout_view'),
    url(r'^forget/$', views.forget_password, name = 'forget_password'),
    # these page who will use the id
    url(r'^Editor/tab-account-change/[0-9]+/[\s\S^/]+/$',views.tab_account_change,name = 'tab_account_change'),
    url(r'^Editor/tab-publication-change/[0-9]+/[\s\S^/]+/$',views.tab_publication_change,name = 'tab_publication_change'),

    # these page who won't use the id
    url(r'^Editor/tab-publication/[\s\S^/]+/$',views.tab_publication,name = 'tab_publication'),
    url(r'^Editor/tab-publication-add/[\s\S^/]+/$',views.tab_publication_add,name = 'tab_publication_add'),
    url(r'^Editor/tab-account-contact/[\s\S^/]+/$',views.tab_account_contact,name = 'tab_account_contact'),
    url(r'^Editor/tab-account-add/[\s\S^/]+/$',views.tab_account_add,name = 'tab_account_add'),
    url(r'^Editor/tab-account/[\s\S^/]+/$',views.tab_account,name = 'tab_account'),

    url(r'^Editor/tab-account-general-change/[\s\S^/]+/$',views.tab_account_general_change,name = 'tab_account_general_change'),

    url(r'^[\s\S^/]+/$',views.toUpload, name = 'toUpload'),
]
