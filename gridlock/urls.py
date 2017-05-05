"""gridlock URL Configuration"""

from django.conf.urls import url
from django.contrib import admin

from preprocessor.views import index

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^example/', index),
]
