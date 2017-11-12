from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^(?P<question_id>[0-9]+)/$', views.question_detail, name='question_detail'),
#    url(r'^$', views.onequestion),
#    url(r'^about$', AboutView.as_view(), name='about'),
]
