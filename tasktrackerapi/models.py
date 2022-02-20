from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token


# Create your models here.

class UserProfileManager(BaseUserManager):

    def create_user(self,email,name,password=None):
        if not email:
            raise ValueError("Please enter valid email")
        email = self.normalize_email(email)
        user = self.model(email=email,name=name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,name,password):
        user = self.create_user(email,name,password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class UserProfile(AbstractBaseUser,PermissionsMixin):

    #id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    is_active = models.BooleanField(default= True)
    is_staff = models.BooleanField(default=False)

    objects=UserProfileManager()

    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['name']


    def _str__(self):
        return self.email


    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender,instance=None,created=False,**kwargs):
        if created:
            Token.objects.get_or_create(user=instance)

class Task(models.Model):
    owner = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    task_name = models.CharField(max_length=100)
    task_description = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status_wip = models.BooleanField()
    status_complete = models.BooleanField(default= False)
    status_reject = models.BooleanField(default=False)
