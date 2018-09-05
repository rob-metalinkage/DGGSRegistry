"""dggsreg URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^dggs_registry$', views.dggs_registry, name='dggs_registry'),
    url(r'^submit_new_dggs$', views.submit_new_dggs, name='submit_new_dggs'),
    url(r'^submit_new_dggs_success$', views.submit_new_dggs_success, name='submit_new_dggs_success'),
    url(r'^review_dggs_spec$', views.select_dggs_spec, name='select_dggs_spec'),
    url(r'^review_dggs_spec/(?P<id>\w+)/$', views.review_dggs_spec, name='review_dggs_spec'),
    url(r'^review_dggs_spec_complete$', views.review_dggs_spec_complete, name='review_dggs_spec_complete'),
    
    url(r'^admin/', admin.site.urls),
]

urlpatterns +=  [ url(r'^skosxl/', include('skosxl.urls')) ]
urlpatterns +=  [ url(r'^rdf_io/', include('rdf_io.urls')) ]

