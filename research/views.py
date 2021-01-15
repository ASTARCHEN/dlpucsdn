# coding=utf-8
from django.shortcuts import render
from account.models import Department


# Create your views here.

def research_index(request, dn):
    d = Department.objects.get(name=dn)
    return render(request, 'research/index.html', {'dn': dn,
                                                   'title': u'%s--科研' % (d.cn),
                                                   'department': d.cn,
                                                   'user': request.user})
