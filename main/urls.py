from django.urls import path
from . import views
from .views import profile_view, edit_profile_view
urlpatterns = [
    path('course', views.index, name='index'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path("logout", views.logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", edit_profile_view, name="edit_profile"),
    path('', views.homepage, name="homepage"),
    path('api/courses/', views.course_list_api, name='course_list_api'),
]