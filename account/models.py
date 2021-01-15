from django.db import models
from django.contrib.auth import get_user_model
from djangohelper.db.models import BaseModel

User = get_user_model()


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    qq = models.CharField(max_length=20, blank=True, null=True)
    number = models.CharField(max_length=15, blank=True, null=True)
    identity = models.IntegerField(default=0)
    deleted = models.BooleanField(default=False)
    website = models.URLField(default="")
    head = models.URLField(default='http://dlpucsdn.qiniudn.com/default.png')

    def __unicode__(self):
        return self.user


class Department(BaseModel):
    name = models.CharField(max_length=5)
    cn = models.CharField(max_length=20)

    def __unicode__(self):
        return self.cn
