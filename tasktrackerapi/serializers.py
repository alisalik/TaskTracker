from rest_framework import serializers
from .models import UserProfile,Task

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('id','email','name','password','designation',)
        extra_kwargs = {
            'password':
            {
                'write_only':True,
                'style':{'input_type':'password'}
            }
        }
    def create(self,validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self,instance,validated_data):
        for attr,value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance,attr,value)
        instance.save()
        return instance

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields=['id','task_name','task_description','status_wip','status_reject','status_complete',]
