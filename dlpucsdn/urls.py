from django.conf.urls import include, url
from django.contrib import admin
import uploader.urls
import account.views
import account.urls
import research.urls
import assignment.urls
import blog.urls
import forum.urls
import news.urls


urlpatterns = [
    url(r'^src/', include(uploader.urls)),
    url(r'^confirm/(?P<t>\S+)/', account.views.confirm_identity, name='confirm_identity'),
    url(r'^$', account.views.index, name='index'),
    url(r'^index/$', account.views.index),
    url(r'^login/', account.views.UserLoginView.as_view, name='login'),
    url(r'^logout/', account.views.user_logout, name='logout'),
    url(r'^signup/', account.views.user_signup, name='signup'),
    url(r'^teacher-signup/', account.views.teacher_signup, name='teacher_signup'),
    url(r'^about/$', account.views.about, name='about'),
    url(r'^admin/', admin.site.urls),
    url(r'^assignment/', include(assignment.urls)),
    url(r'^user/', include(account.urls)),
    url(r'^(?P<dn>\w{2,3})/research/', include(research.urls)),
    url(r'^(?P<dn>\w{2,3})/blog/', include(blog.urls)),
    url(r'^(?P<dn>\w{2,3})/forum/', include(forum.urls)),
    url(r'^(?P<dn>\w{2,3})/', include(news.urls)),

]
