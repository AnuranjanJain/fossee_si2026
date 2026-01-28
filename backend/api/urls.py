"""
URL routing for the API.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    
    # Data operations
    path('upload/', views.UploadCSVView.as_view(), name='upload'),
    path('equipment/', views.EquipmentListView.as_view(), name='equipment-list'),
    path('summary/', views.SummaryView.as_view(), name='summary'),
    path('history/', views.HistoryListView.as_view(), name='history'),
    
    # Reports
    path('report/pdf/', views.PDFReportView.as_view(), name='pdf-report'),
]
