from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('post/detail/<slug:slug>/',views.post_detail, name='detail'),
    path('post/post_topic/<str:pk>/', views.post_topic, name='post-topic'),
    path('post/create/', views.post_creation,name='create_post')
]