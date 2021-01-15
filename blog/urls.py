from django.conf.urls import include, url
from blog.views import blog_index, write_blog, blog_view, create_breply, del_blog

urlpatterns = [
    url(r'^$', blog_index, name='blog_index'),
    url(r'^write/$', write_blog, name='write_blog'),
    url(r'^(?P<blog_id>\d+)/$', blog_view, name='blog_view'),
    url(r'^(?P<blog_id>\d+)/reply/$', create_breply, name='create_breply'),
    url(r'^(?P<blog_id>\d+)/del/$', del_blog, name='del_blog'),
]
