from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    path('',views.home, name='home'),
    path('trimm/',views.trimm, name='trimm'),
    path('video_feed/<str:style_name>/', views.video_feed_view, name='video_feed'),
    path('virtual/',views.virtual, name='virtual'),
  #  path('video_feed/<str:style_name>/', views.video_feed_view, name='video_feed'),

    path('ai/',views.ai, name='ai'),

]