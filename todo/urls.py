from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),  # updated
    path('todopage/', views.todo, name='todopage'),
    path('delete_todo/<int:srno>/', views.delete_todo, name='delete_todo'),
    path('signout/', views.signout, name='signout'),
]