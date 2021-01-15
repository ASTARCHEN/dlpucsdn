from django.conf.urls import include, url
from assignment.views import assignment_index, assignment_issue

urlpatterns = [
    url(r'^$', assignment_index, name='assignment_index'),
    url(r'^issue/$', assignment_issue, name='issue')
]
