from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hello', views.hello_world, name='hello'),
    path('worker', views.worker_test, name='worker_test'),
    path('worker_api', views.worker_api, name='worker_api'),
]