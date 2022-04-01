from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('message/<str:pk>/', views.message, name="message"),

    path('create-message/', views.createMessage, name="create-message"),
    path('store/', views.store, name="store"),
    path('profile/', views.profile, name="profile"),
    path('leaderboard/', views.leaderboard, name="leaderboard"),

]