from django.contrib.auth import get_user_model
from django.db import models
from djangohelper.db.models import BaseModel

from account.models import Department

UserModel = get_user_model()


# Create your models here.
class Blogs(BaseModel):
    auth = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    department_name = models.ForeignKey(Department, on_delete=models.CASCADE)
    # node = models.ForeignKey(node)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    click = models.IntegerField(default=0)
    reply_count = models.IntegerField(default=0)
    time_created = models.DateTimeField(auto_now_add=True)
    yo = models.IntegerField(default=0)
    deleted = models.BooleanField(default=False)

    class Meta():
        ordering = ['-time_created']

    def __unicode__(self):
        return self.title


class Breply(BaseModel):
    auth = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    topic = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    yo = models.IntegerField(default=0)
    content = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['time_created']
