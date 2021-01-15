from django.db import models
from account.models import Department
from django.contrib.auth import get_user_model
from djangohelper.db.models import BaseModel

UserModel = get_user_model()


# Create your models here.
class Departments(BaseModel):
    name = models.CharField(max_length=20)
    grade = models.IntegerField()
    college = models.CharField(max_length=20)
    url = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return self.cn
