from django.urls import path

from . import views

app_name = 'mf'

urlpatterns = [
    path('addisin', views.ISINCreate.as_view(), name='create-isin'),
    path('chart/<str:pk>/', views.line_chart, name='line_chart'),
    path('chartJSON/<str:pk>/', views.line_chart_json, name='line_chart_json'),
]

  