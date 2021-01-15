from django.conf.urls import include, url
from forum.views import forum_index, create_reply, create_topic, topic_view, del_topic

urlpatterns = [
    url(r'^$', forum_index, name='forum_index'),
    url(r'^create/$', create_topic, name='create_topic'),
    url(r'^(?P<topic_id>\d+)/$', topic_view, name='topic_view'),
    url(r'^(?P<topic_id>\d+)/reply$', create_reply, name='create_reply'),
    url(r'^(?P<topic_id>\d+)/delete$', del_topic, name='del_topic'),
]
