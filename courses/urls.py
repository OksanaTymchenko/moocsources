from django.conf.urls import include, url
from django.contrib import admin
from courses_site import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^courses/', include('courses_site.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^signup/', views.signup),
    url(r'^login/', views.home),
    url(r'^logout/', views.out),
    url(r'^index/', views.index),
    url(r'^saveq/', views.saveq),
    url(r'^like/(?P<course_id>[0-9]+)/$', views.like, name='like'),
    url(r'^favorite/(?P<course_id>[0-9]+)/$', views.favorite, name='favorite'),
    url(r'^favlist/', views.favlist),
    url(r'^profile/', views.adminProfile),
    url(r'^search/', views.search),
    url(r'^emailing/', views.emailing),
    url(r'^recommend/', views.recommendations),
    url(r'^regenerate/', views.regenerate),
    url(r'^questionnaire/', views.loadInfo),
    url(r'^user_account/', views.user_account),
]

api_urls = [
    url(r'^accounts/$', views.AccountList.as_view()),
    url(r'^accounts/(?P<pk>[0-9]+)/$', views.AccountDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^courses_json/$', views.CourseList.as_view()),
    url(r'^courses_json/(?P<pk>[0-9]+)/$', views.CourseDetail.as_view()),
    url(r'^questionnaire_json/$', views.QuestionnaireList.as_view()),
    url(r'^questionnaire_json/(?P<pk>[0-9]+)/$', views.QuestionnaireDetail.as_view()),

]

api_urls = format_suffix_patterns(api_urls)

urlpatterns += api_urls
