from django.conf.urls import url
from . import views

app_name = 'order'
urlpatterns = [
    url(r'^create/$', views.OrderCreate, name='OrderCreate'),
]
