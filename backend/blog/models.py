from django.db import models


class User(models.Model):
    # unique=True 用户名不能重复
    u_id = models.AutoField(primary_key=True)
    u_name = models.CharField(max_length=32, unique=True)
    avatar = models.ImageField(upload_to='static/avatar/', blank=True, null=True, default='static/avatar/avatar.png')
    total_likes = models.IntegerField(default=0)
    total_comments = models.IntegerField(default=0)
    registration_date = models.DateTimeField(auto_now=True)
    u_password = models.CharField(max_length=256)
    u_mail = models.CharField(max_length=256, null=True)
    is_super = models.BooleanField(default=False)


class Blog(models.Model):
    blog_id = models.AutoField(primary_key=True)
    u_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True)
    content = models.TextField(null=True)
    image = models.ImageField(upload_to='static/blog_images/', blank=True, null=True)
    comments = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    likes_user = models.CharField(max_length=1000, null=True)
    favorite_user = models.CharField(max_length=1000, null=True)
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    c_id = models.AutoField(primary_key=True)
    u_id = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_id = models.IntegerField(null=True)
    content = models.TextField(null=True)
    created_time = models.DateTimeField(auto_now_add=True)
