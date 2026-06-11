from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectListView.as_view()),
    path('<int:pk>/', views.ProjectDetailView.as_view()),
    path('tasks/', views.TaskListView.as_view()),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view()),
    path('tasks/<int:task_id>/comments/', views.CommentView.as_view()),
    path('sprints/', views.SprintListView.as_view()),
    path('ai/breakdown/', views.AITaskBreakdownView.as_view()),
    path('ai/sprint-plan/', views.AISprintPlanView.as_view()),
    path('dashboard/', views.DashboardView.as_view()),
]