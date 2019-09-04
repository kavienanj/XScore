from django.urls import path
from . import views

urlpatterns = [
    path('mcq/', views.mcq_paper, name='mcq'),
    path('essay/', views.essay_paper, name='essay'),
    path('essay/<int:id>/', views.download_essay, name='download_essay'),
    path('admin-dashboard/', views.admin_dashboard, name='dashboard'),
    path('admin-dashboard/create/', views.create_paper, name='create_paper'),
    path('admin-dashboard/create/<int:id>/', views.create_paper, name='create_paper'),
    path('', views.home, name='home')
]
