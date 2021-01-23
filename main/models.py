from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import  get_user_model
from django.urls import reverse
from tinymce import HTMLField


User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()
    
    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=50)
    
    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = HTMLField()
    comment_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
    featured = models.BooleanField(default=False)
    thumbnail = models.ImageField(null=True, blank=True)
    previous_post = models.ForeignKey('self', related_name="previous",  on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey('self', related_name="next", on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={
            'id': self.id
        })
    
    def get_update_url(self):
        return reverse('update', kwargs={
            'id': self.id
        })
    
    def get_delete_url(self):
        return reverse('delete', kwargs={
            'id': self.id
        })
    
    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.user.username