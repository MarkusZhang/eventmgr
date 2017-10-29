from django.conf.urls import patterns, include, url
from django.contrib import admin

from views import index
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',index,name='index'),
    url(r'^eventinfo/', include('eventinfo.urls')),
    url(r'^eventorg/', include('eventmgr.urls')),
    url(r'^account/', include('account.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
