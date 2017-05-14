from . import views
from django.conf.urls import url

app_name = 'stopgenerator'
urlpatterns = [
    url(r'^generate_stop_layout', views.generate_stop_layout, name='generate_stop_layout'),
]
