"""gridlock URL Configuration"""

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='demo.html'), name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^preprocessor/', include('preprocessor.urls')),
    url(r'^stopgenerator/', include('stopgenerator.urls')),
    url(r'^routegenerator/', include('routegenerator.urls')),
    url(r'^networkoptimizer/', include('networkoptimizer.urls')),
]
