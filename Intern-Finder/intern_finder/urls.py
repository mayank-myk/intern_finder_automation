from django.conf.urls import include, url
from django.contrib import admin
from intern.views import *
urlpatterns = [
    # Examples:
    # url(r'^$', 'intern_finder.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', index,name='index'),
]
