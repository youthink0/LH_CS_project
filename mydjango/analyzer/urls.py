from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='analyzer-home'),
    path('result/', views.result, name='analyzer-result'),
    path('result/pos', views.positive, name='analyzer-positive'),
    path('result/neg', views.negative, name='analyzer-Negative'),
    path('about/', views.about, name='analyzer-about'),
]
