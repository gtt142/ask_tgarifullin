"""ask_tgarifullin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.http import HttpResponse, Http404
from questions import views
def err404(request):
	raise Http404("PageNotFound")

urlpatterns = [
    url(r'^test_gunicorn/?$', views.test_gu),
    url(r'^$', views.index, name='index'),
    url(r'^hot/$', views.hot, name='hot'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^admin/', admin.site.urls),
    url(r'^question/', include('questions.urls')),
    url(r'^userset/', views.userset, name='userset'),
    url(r'^ask/', views.ask, name='ask'),
    url(r'^tag/(?P<tag_word>\w+)/$', views.tag, name='tag_detail'),
    url(r'^', err404),
]
