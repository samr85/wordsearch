
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('asdf/<str:id>', views.detail, name='detail'),
    path('grid', views.grid, name='grid'),
    ]
