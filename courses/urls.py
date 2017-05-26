from django.conf.urls import include, url
from django.contrib import admin
from courses_site import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^courses/', include('courses_site.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^signup/', views.signup),
    url(r'^login/', views.home),
    url(r'^logout/', views.out),
    url(r'^index/', views.index, name='index'),
    url(r'^saveq/', views.saveq),
    url(r'^like/(?P<course_id>[0-9]+)/$', views.like, name='like'),
    url(r'^favorite/(?P<course_id>[0-9]+)/$', views.favorite, name='favorite'),
    url(r'^favlist/', views.favlist),
    url(r'^recommend/', views.recommendations),
    url(r'^regenerate/', views.regenerate),
    url(r'^profile/', views.adminProfile),
    url(r'^search/', views.search),
    url(r'^emailing/', views.emailing),
]