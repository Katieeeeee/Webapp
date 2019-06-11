"""Defines URL patterns for eLearn."""

from django.urls import path
from . import views

app_name = "eLearn"

urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    
    path('<int:course_id>/main/', views.main, name='main'),
    path('main/', views.main, name='main'),

    path('list/', views.CourseListView.as_view(), name='list_course'),
    path('create/', views.CourseCreateView.as_view(), name='create_course'),
    path('<pk>/edit/', views.CourseUpdateView.as_view(), name='edit_course'),
    path('<pk>/delete/', views.CourseDeleteView.as_view(), name='delete_course'),

    path('<int:course_id>/listvideos/', views.list_video, name='list_video'),
    path('<int:course_id>/createvideo/', views.create_video, name='create_video'),
    path('<int:video_id>/editvideo/', views.edit_video, name='edit_video'),
    path('<int:video_id>/deletevideo/', views.delete_video, name='delete_video')
]
