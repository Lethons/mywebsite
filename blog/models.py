from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Tag(models.Model):
    """ blog tag models """
    tag = models.CharField(max_length=10)

    def __str__(self):
        return self.tag


class Blog(models.Model):
    """ blog models """
    title = models.CharField(max_length=50)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING)
    publish_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        # order by -publish_time
        ordering = ['-publish_time']