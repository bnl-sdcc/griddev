from django.conf.urls.defaults import *
# official/vital
from mdsite.views import dataquery_search, dataquery_analysis 
# for testing/development
from mdsite.views import current_datetime, rpy_test

urlpatterns = patterns('',
    # Example:
    #(r'^mariachi-ws/', include('mdsite.urls')),
    (r'^mariachi-ws/django/current_datetime/$', current_datetime),
    #(r'^mariachi-ws/data_search/$', data_search),
    (r'^mariachi-ws/django/dataquery/$', dataquery_search),
    (r'^mariachi-ws/django/analysis/$', dataquery_analysis),
    (r'^mariachi-ws/django/rpytest/$', rpy_test),
    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
    # Uncomment for static media path for development
    (r'^static/(?P<path>.*)$', 
         'django.views.static.serve', 
         {'document_root': '/home/jhover/devel/mariachi-data-ws/static/'}
        ),
)
