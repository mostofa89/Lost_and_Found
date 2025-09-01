from django.urls import path
from .import views

app_name = 'reports'

urlpatterns = [
    path('lost_reports/', views.lost_reports_view, name='lost_reports'),
]