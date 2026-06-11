from django.urls import path
from . import views

urlpatterns = [
    path('', views.TeamListView.as_view()),
    path('<int:pk>/', views.TeamDetailView.as_view()),
    path('<int:pk>/add-member/', views.AddMemberView.as_view()),
]