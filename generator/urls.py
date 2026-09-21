from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('generate/', views.generate_view, name='generate'),
    path('history/', views.history_view, name='history'),
    path('generation/<int:pk>/', views.detail_view, name='detail'),
    path('generation/<int:pk>/download/', views.download_view, name='download'),
    path('generation/<int:pk>/delete/', views.delete_view, name='delete'),
]
