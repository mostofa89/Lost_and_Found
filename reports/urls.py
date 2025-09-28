from django.urls import path
from .import views

app_name = 'reports'

urlpatterns = [
    path('lost_reports/', views.lost_reports_view, name='lost_reports'),
    path('found_reports/', views.found_reports_view, name='found_reports'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('claim/', views.claim_view, name='claim'),
]