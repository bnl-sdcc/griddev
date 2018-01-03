from django.conf.urls.defaults import *
from mdsite.views import current_datetime, dataquery_search, rpy_test

urlpatterns = patterns('',
    # Example:
    #(r'^mariachi-ws/', include('mdsite.urls')),
    (r'^mariachi-ws/django/current_datetime/$', current_datetime),
    #(r'^mariachi-ws/data_search/$', data_search),
    (r'^mariachi-ws/django/dataquery/$', dataquery_search),
    (r'^mariachi-ws/django/rpytest/$', rpy_test), 
    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
    # Uncomment for static media path for development
    (r'^mariachi-ws/django/mariachi-media/(?P<path>.*)$', 
     'django.views.static.serve', 
     {'document_root': '/home/jhover/devel/mariachi-data-ws/static/'}),
)
