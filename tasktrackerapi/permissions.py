from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):

    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user==request.user

class UpdateOwnTask(permissions.BasePermission):

    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner==request.user

        '''if obj.id==request.user.id:
            return True'''
