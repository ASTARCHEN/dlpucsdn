# coding=utf-8
from django.contrib.auth import get_user_model
from django.db import models
from djangohelper.db.models import BaseModel

UserModel = get_user_model()


class Files(BaseModel):
    auth = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.TextField()
    url = models.URLField(default='')
    upload_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-upload_time']
