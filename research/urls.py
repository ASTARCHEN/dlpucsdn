from django.conf.urls import include, url
from research.views import research_index

urlpatterns = [
    url(r'^$', research_index, name='research_index'),
]
