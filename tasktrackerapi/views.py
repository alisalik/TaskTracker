from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import UserProfile,Task
from tasktrackerapi.permissions import UpdateOwnProfile,UpdateOwnTask
from .serializers import UserSerializer,TaskSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.db.models import Q




# Create your views here.
class GetUserInfo(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    '''def get_queryset(self):
        user=self.request.user
        user1 = UserProfile.objects.filter(name=user)
        return(user1)'''
    #permission_classes = (ReadUpdateOwnProfile)


class UserRegisterView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    #permission_classes = (IsAuthenticated,ReadUpdateOwnProfile,)

    def create(self,request,*args,**kwargs):
        data={}
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            info=serializer.save()
            data['response'] = "successfully created account"
            data['email'] = info.email
            data['name'] = info.name
            token = Token.objects.get(user=info).key
            data['token'] = token
        else:
            return Response(serializer.errors)
        return Response(data)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,UpdateOwnProfile,)

class LoginView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class TasklistView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer

    def get_queryset(self):
        user=self.request.user
        task = Task.objects.filter(owner=user)
        return (task)



class CreateTaskView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,UpdateOwnTask,)

    def create(self,request,*args,**kwargs):
        user = request.user
        task = Task(owner=user)
        serializer = TaskSerializer(task,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class UpdateTaskView(generics.RetrieveUpdateAPIView):
    serializer_class = TaskSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,UpdateOwnTask,)
    #queryset = Task.objects.all()

    def get_queryset(self):
        user=self.request.user
        task = Task.objects.filter(owner=user)
        return (task)

    def update(self,request,*args,**kwargs):
        user = request.user
        task = Task.objects.filter(owner=request.user)
        if task.owner != user:
            return Response("You dont have permission to edit task")
        serializer = self.serializer_class(data=request.data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class DeleteTaskView(generics.RetrieveDestroyAPIView):
    serializer_class=TaskSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,UpdateOwnTask)

    def get_queryset(self):
        user = self.request.user
        task = Task.objects.filter()
        return task
    #return Response("Task has been deleted")

    def delete(self,request,*args,**kwargs):

        task = Task.objects.filter(owner=request.user)
        user = request.user
        if task.owner!=user:
            return Response ("You dont have permission to delete this post")
        instance=self.get_object()
        instance.delete()
