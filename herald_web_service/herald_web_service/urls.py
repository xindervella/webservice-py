from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from curriculum_service.views import parserHtml
from tyx_service.views import tyxPc

urlpatterns = patterns('',
    # Examples:
    url(r'^herald_web_service/$', 'herald_web_service.views.home', name='home'),
    url(r'^herald_web_service/curriculum/([\w]+)/([\w-]+)/$', parserHtml),
    url(r'^herald_web_service/tyx/([\w]+)/([\w]+)/$', tyxPc),

    # url(r'^herald_web_service/', include('herald_web_service.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)