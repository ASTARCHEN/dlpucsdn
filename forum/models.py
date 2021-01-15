from django.contrib.auth import get_user_model
from django.db import models
from djangohelper.db.models import BaseModel

from account.models import Department

UserModel = get_user_model()


# Create your models here.
class Topic(BaseModel):
    auth = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    click = models.IntegerField(default=0)
    reply_count = models.IntegerField(default=0)
    time_created = models.DateTimeField(auto_now_add=True)
    last_replied = models.DateTimeField(auto_now_add=True, editable=True)
    deleted = models.BooleanField(default=False)
    department_name = models.ForeignKey(Department, on_delete=models.CASCADE)
    yo = models.IntegerField(default=0)

    # node = models.ForeignKey(node,default='all')
    class Meta():
        ordering = ['-last_replied']

    def __unicode__(self):
        return self.title


class Reply(BaseModel):
    auth = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    time_created = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    yo = models.IntegerField(default=0)

    class Meta():
        ordering = ['time_created']

    def __unicode__(self):
        return str(self.id) + self.topic.title


class Mention(BaseModel):
    sender = models.ForeignKey(UserModel, related_name='send', on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserModel, related_name='receive', on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    topic_name = models.ForeignKey(Topic, blank=True, null=True, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    read = models.BooleanField(default=False)

    def __unicode__(self):
        return self.topic_name
