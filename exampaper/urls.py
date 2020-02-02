from django.urls import path
from . import views

urlpatterns = [
    path('mcq/', views.mcq_paper, name='mcq'),
    path('essay/', views.essay_paper, name='essay'),
    path('essay/<int:id>/<str:kind>/', views.download_essay, name='download_essay'),
    path('admin-dashboard/', views.admin_dashboard, name='dashboard'),
    path('admin-dashboard/create/', views.create_paper, name='create_paper'),
    path('admin-dashboard/create/<int:id>/', views.create_paper, name='create_paper'),
    path('admin-dashboard/add/<int:id>/<str:typ>/', views.add_question, name='add_question'),
    path('admin-dashboard/add/<int:id>/<str:typ>/<int:q_id>/', views.add_question, name='edit_question'),
    path('admin-dashboard/rem/<str:typ>/<int:id>/', views.remove_question, name='delete_question'),
    path('admin-dashboard/viewpaper/<int:id>/', views.view_paper, name='view_paper'),
    path('admin-dashboard/<int:id>/', views.leader_board, name='leaderboard'),
    path('', views.home, name='home')
]
