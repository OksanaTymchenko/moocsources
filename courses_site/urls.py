from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.allcourses, name='index'),
    url(r'^(?P<course_id>[0-9]+)/$', views.detail, name='detail'),

    # url(r'^(?P<param>[%&+ \w]+)/$', views.filtered, name='filtered')

]