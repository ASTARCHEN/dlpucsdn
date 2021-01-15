from django.conf.urls import include, url
from account.views import *

urlpatterns = [
    url(r'^(?P<user_id>\d+)/$', user_profile, name='user_profile'),
    url(r'^head/$', user_head, name='user_head'),
    url(r'^edit/(?P<user_id>\d+)/$', edit_profile, name='edit_profile'),
]
