from django.urls import path

from MRSapp import views

app_name = 'mrs_app'

urlpatterns = [
    path('', views.index, name='search'),
]