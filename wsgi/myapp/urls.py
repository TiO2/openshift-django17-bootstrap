from django.conf.urls import patterns, include, url

from myapp import views

urlpatterns = patterns('',
    url(r'^$', views.Index.as_view(), name='index'),
    
)
