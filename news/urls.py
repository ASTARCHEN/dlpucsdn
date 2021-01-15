from django.conf.urls import include, url
from news.views import add_news, news_count, news_index

urlpatterns = [
    url(r'add/$', add_news, name='add_news'),
    url(r'^$', news_index, name='news_index'),
    url(r'(?P<id>\d+)/$', news_count, name='news_count')
]
