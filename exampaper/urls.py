from django.urls import path
from . import views

urlpatterns = [
    path('quiz/<int:id>/', views.mcq_paper, name='mcq'),
    path('admin-dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/create/', views.create_paper, name='create_paper'),
    path('admin-dashboard/create/<int:id>/', views.create_paper, name='create_paper'),
    path('admin-dashboard/add/<int:id>/', views.add_question, name='add_question'),
    path('admin-dashboard/add/<int:id>/<int:q_id>/', views.add_question, name='edit_question'),
    path('admin-dashboard/add/<int:id>/<int:q_id>/<str:del_q>/', views.add_question, name='delete_question'),
    path('admin-dashboard/viewpaper/<int:id>/', views.view_paper, name='view_paper'),
    path('admin-dashboard/<int:id>/', views.leader_board, name='leaderboard'),
    path('', views.home, name='home')
]
