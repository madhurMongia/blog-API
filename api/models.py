from django.template.defaultfilters import slugify
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from core.settings import AUTH_USER_MODEL

class Catagory(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Post(models.Model):

    title = models.CharField(max_length=250)
    content = models.TextField()
    isPublished = models.BooleanField(default=False)
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete= models.PROTECT)
    slug = models.SlugField(blank = True)
    category = models.ForeignKey( Catagory , on_delete=models.CASCADE)
    date_created = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post ,self).save(*args, **kwargs)
