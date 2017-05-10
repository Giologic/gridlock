from . import views
from django.conf.urls import url


app_name = 'preprocessor'
urlpatterns = [
    url(r'^location_list/$', views.location_list, name='location_list'),
    url(r'^location_geometry/', views.location_geometry, name='location_geometry')
]
