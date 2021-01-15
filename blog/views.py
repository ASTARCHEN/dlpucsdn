# coding=utf-8
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from account.models import Department
from blog.models import Blogs, Breply
from django.urls import reverse
from django.template import RequestContext
from django.contrib import messages
from django.utils.translation import ugettext as _


# Create your views here.

def write_blog(request, dn):
    d = Department.objects.get(name=dn)
    if request.method == 'GET':
        return render(request, 'blog/write.html', {'user': request.user,
                                                   'dn': dn,
                                                   'title': u'书写自己的博客吧--工大CSDN俱乐部',
                                                   'department': d.cn},
                      context_instance=RequestContext(request))
    elif request.method == 'POST':
        b = Blogs()
        b.auth = request.user
        b.title = request.POST['title']
        b.content = request.POST['content']
        b.department_name = d
        if b.title and b.content:
            b.save()
            return HttpResponseRedirect(reverse('blog_index', kwargs={'dn': dn}))
        messages.add_message(request, messages.WARNING, _(u'标题或内容不能为空！'))
        return HttpResponseRedirect(reverse('write_blog', kwargs={'dn': dn}))


def blog_view(request, dn, blog_id):
    d = Department.objects.get(name=dn)
    b = Blogs.objects.get(id=blog_id)
    b.click += 1
    b.save()
    br = Breply.objects.filter(topic=blog_id)
    return render(request, 'blog/view.html', {'user': request.user,
                                              'blog': b,
                                              'request': request,
                                              'dn': dn,
                                              'title': u'%s' % (b.title),
                                              'breply': br,
                                              'blog_id': blog_id,
                                              'department': d.cn},
                  context_instance=RequestContext(request))


def blog_index(request, dn):
    d = Department.objects.get(name=dn)
    blog = Blogs.objects.filter(department_name=d, deleted=False)
    return render(request, 'blog/index.html', {'dn': dn,
                                               'blog': blog,
                                               'title': u'博客列表',
                                               'user': request.user,
                                               'department': d.cn},
                  context_instance=RequestContext(request))


def create_breply(request, dn, blog_id):
    if request.method == 'POST':
        b = Blogs.objects.get(id=blog_id)
        br = Breply()
        br.auth = request.user
        br.content = request.POST['content']
        br.topic = b
        br.save()
        b.click -= 1
        b.reply_count += 1
        b.save()
        return HttpResponseRedirect(reverse('blog_view', kwargs={'dn': dn,
                                                                 'blog_id': blog_id}))


def del_blog(request, dn, blog_id):
    b = Blogs.objects.get(id=blog_id)
    if request.user == b.auth:
        b.deleted = True
        b.save()
        messages.add_message(request, messages.SUCCESS, _(u'删除成功 !'))
    else:
        messages.add_message(request, messages.WARNING, _(u'删除失败，你不是这篇博客的作者 !'))
    return HttpResponseRedirect(reverse('blog_index', kwargs={'dn': dn}))

# def blog_chart(request):
