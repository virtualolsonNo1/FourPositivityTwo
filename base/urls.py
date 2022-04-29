from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
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
    path('settings/', views.settings, name="settings"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)