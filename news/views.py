# coding=utf-8
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from account.models import Department
from django.urls import reverse
from news.models import List
from django.contrib import messages
from django.utils.translation import ugettext as _


def add_news(request, dn):
    d = Department.objects.get(name=dn)
    if request.method == 'GET':
        return render(request, 'news/add.html', {'user': request.user,
                                                 'dn': dn,
                                                 'title': '添加一条新闻',
                                                 'department': d.cn},
                      context_instance=RequestContext(request))
    elif request.method == 'POST':
        n = List()
        title = request.POST['title']
        url = request.POST['url']
        auth = request.user
        if title and url:
            n.title = title
            n.url = url
            n.auth = auth
            n.department_name = d
            n.save()
        else:
            messages.add_message(request, messages.WARNING, _(u'标题或链接不能为空'), )
            return HttpResponseRedirect(reverse('add_news', kwargs={'dn': dn}))
    return HttpResponseRedirect(reverse('news_index', kwargs={'dn': dn}))


def news_index(request, dn):
    if Department.objects.filter(name=dn).exists():
        d = Department.objects.get(name=dn)
        new = List()
        new.department_name = d
        news = List.objects.filter(department_name=d)
        return render(request, 'news/list.html', {'user': request.user,
                                                  'dn': dn,
                                                  'title': u'News %s' % (d.cn),
                                                  'news': news,
                                                  'department': d.cn},
                      context_instance=RequestContext(request))
    return HttpResponseRedirect(reverse('index'))


def news_count(request, dn, id):
    n = List.objects.get(id=id)
    if not n.auth == request.user:
        n.click += 1
    url = n.url
    n.save()
    return HttpResponseRedirect(url)
