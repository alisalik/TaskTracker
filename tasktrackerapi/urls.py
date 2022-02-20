from django.urls import path
from .views import GetUserInfo,UserRegisterView,UserDetailView,LoginView,CreateTaskView,UpdateTaskView,UpdateTaskView,TasklistView,DeleteTaskView

urlpatterns = [
    path('userinfo/',GetUserInfo.as_view()),
    path('register/',UserRegisterView.as_view()),
    path('update/<int:pk>',UserDetailView.as_view()),
    path('login/',LoginView.as_view()),
    path('taskview',TasklistView.as_view()),
    path('taskcreate/',CreateTaskView.as_view()),
    path('updatetask/<int:pk>',UpdateTaskView.as_view()),
    path('deletetask/<int:pk>',DeleteTaskView.as_view()),
]
