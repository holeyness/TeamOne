# myapp/api.py
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from poster.models import *

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username', 'first_name', 'last_name', 'last_login']
        authorization= DjangoAuthorization()

class PostResource(ModelResource):
    # user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Post.objects.all()
        resource_name = 'post'
        authorization= DjangoAuthorization()

class UserPostResource(ModelResource):
    post = fields.ForeignKey(PostResource, 'post_id')
    user = fields.ForeignKey(UserResource, 'user_id')

    class Meta:
        queryset = user_post.objects.all()
        resource_name = 'user_post'
        authorization= DjangoAuthorization()