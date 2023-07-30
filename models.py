from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Topics(models.Model):
    name = models.CharField(max_length=30, unique = True)
    def __str__(self):
        return self.name

class Posts(models.Model):
    title = models.CharField(max_length = 100, unique= True)
    content = RichTextUploadingField() 
    views = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete= models.CASCADE, default= None)
    image = models.ImageField(null=True, blank= True , max_length=1000)
    published = models.BooleanField(default=False)
    slug = models.SlugField(null=True,)
    created_at = models.DateTimeField(auto_now_add= True)
    post_topic = models.ForeignKey(Topics, on_delete= models.CASCADE, null = True)

    def __str__(self):
        return self.title

    # def snippet(self):
    #     return self.content[:130]





