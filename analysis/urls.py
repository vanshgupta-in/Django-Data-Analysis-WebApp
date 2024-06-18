from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('analyze/<int:file_id>/', views.analyze_file, name='analyze_file'),
]
