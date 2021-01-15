from django.conf.urls import include, url
from uploader.views import src_index, upload_file, receive_url

# patterns('uploader.views',
urlpatterns = [
    url(r'^$', src_index, name='src_index'),
    url(r'^upload/$', upload_file, name='upload_file'),
    url(r'^receive/$', receive_url, name='receive_url'),
]
