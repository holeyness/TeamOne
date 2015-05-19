from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    
    #Primary key is automatically generated
    title = models.CharField(max_length = 200)

    #this will allow you to see the title as like the name of the post
    def __str__(self):
        return self.title

    description = models.CharField(max_length = 300)
    image = models.FileField(upload_to='post_image', blank = True, null = True)
    data_type = models.IntegerField() # 0 is image, 1 is text
    created_date = models.DateTimeField('Post Created On')
    modified_date = models.DateTimeField('Post Modified On')
    last_liked_date = models.DateTimeField('Post Last Liked On', null=True, auto_now_add=True)
    num_likes = models.IntegerField(default=0)


class user_post(models.Model):

    user_id = models.ForeignKey(User)
    post_id = models.ForeignKey('Post')
    permission = models.IntegerField() #0 is only me, 1 is followers, 2 is global

class Like(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey('Post')
    date = models.DateTimeField(auto_now_add=True)
