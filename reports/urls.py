from django.urls import path
from .import views

app_name = 'reports'

urlpatterns = [
    path('lost_reports/', views.lost_reports_view, name='lost_reports'),
    path('lost_items/', views.lost_items_view, name='lost_items'),
    path('found_reports/', views.found_reports_view, name='found_reports'),
    path('found_items/', views.found_items_view, name='found_items'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('claim/<int:pk>/', views.claim_view, name='claim'),

]