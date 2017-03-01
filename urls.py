from django.conf.urls import url

from . import views


app_name = 'ftsefinance'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^status/', views.status, name='status'),
    url(r'^(?P<ticker>[A-Za-z:A-Za-z]+)/$', views.plot, name='plot')
]
