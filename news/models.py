from django.db import models
from django.contrib.auth.models import User
from account.models import Department
from djangohelper.db.models import BaseModel
from django.contrib.auth import get_user_model
from djangohelper.db.models import BaseModel

UserModel = get_user_model()


# Create your models here.
class List(BaseModel):
    auth = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.TextField(max_length=100)
    url = models.URLField()
    time_created = models.DateTimeField(auto_now_add=True)
    click = models.IntegerField(default=0)
    department_name = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-time_created']

    def __unicode__(self):
        return self.title
