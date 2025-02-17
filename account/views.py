#coding=utf-8

from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from account.models import Profile
from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.urls import reverse
from astartool.string import to_text as _
from astartool.string.password_check import check_length
from django.core.mail import send_mail, mail_admins
from forum.models import Topic
import base64
import json
import sys
import re
import qiniu.config
# import qiniu.rs
# import qiniu.io
from django.views import View
qiniu.config.ACCESS_KEY = "vco8VEaZwm24oxn9btpSdjVUMGUe21-K049IlIbl"
qiniu.config.SECRET_KEY = "jTUDwXmbx8uzSG-jEXAfigbQN8Aj3Q3-K6eDU6Ru"

class UserLoginView(View):
    def get(self, request):
        return render(request, 'account/login.html', {'title': '用户登录--工大CSDN俱乐部'})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        u = authenticate(username=username, password=password)
        if not User.objects.filter(username=username).exists():
            messages.add_message(request, messages.WARNING, u'用户名不存在')
            return render(request, 'account/login.html', {'login': False})

        elif not u:
            messages.add_message(request, messages.WARNING, u'用户名和密码不符')
            return render(request, 'account/login.html')
        login(request, u)
        messages.add_message(request, messages.WARNING, u'你已登录')
        return HttpResponseRedirect(reverse('index'))



def user_signup(request):
    if request.method == 'GET':
        return render(request, 'account/signup.html', {'title': u'学生注册--工大CSDN俱乐部'},)
    elif request.method == 'POST':
        username = request.POST['username']
        number = request.POST['number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if check_length(username, 5):
            messages.add_message(request, messages.WARNING, _(u'用户名长度不能少于6位，请重新输入'))
            return render(request, 'account/signup.html')
        if check_length(number, 10):
            messages.add_message(request, messages.WARNING, _(u'输入的学号有误，请重新输入'))
            return render(request, 'account/signup.html')
        if check_length(password1, 6) :
            messages.add_message(request, messages.WARNING, _(u'密码过短，至少6位'))
            return render(request, 'account/signup.html',
                                      context_instance=RequestContext(request))
        if Profile.objects.filter(number = number).exists():
            messages.add_message(request, messages.WARNING, _(u'输入的学号已被注册，请重新输入或联系作者'))
            return render(request, 'account/signup.html')
        if password1 == '123456':
            messages.add_message(request, messages.WARNING, _(u'输入的密码过于简单，请重新输入'))
            return render(request, 'account/signup.html')
        if password1 == password2:
            user = User.objects.create_user(username=username, password=password1,email=email)
            u = authenticate(username=username, password=password1)
            messages.add_message(request, messages.WARNING, _(u'注册成功'))
        else:
            messages.add_message(request, messages.WARNING, _(u'密码不一致，请重新输入'))
            return render(request, 'account/signup.html')
        login(request, u)
        p = Profile()
        p.number = number
        p.username = username
        p.user = user
        p.save()
        return HttpResponseRedirect(reverse('index'))


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def index(request):
    topics = Topic.objects.filter(deleted = False)[:20]
    return render(request, 'index.html', {'user': request.user,
                                             'request': request,
                                             'topic':topics,
                                             'title': _(u'大连工业大学CSDN高校俱乐部')})


def about(request):
    return render(request, 'about.html')

def user_profile(request, user_id):
    p = User.objects.get(id=user_id)
    file = qiniu.rs.PutPolicy('dlpucsdn')
    file.returnUrl = "http://127.0.0.1:8000/user/head/"
    token = file.token()
    key = ''
    if request.method == 'POST':
        local_file = '%s' % __file__
        ret, err = qiniu.io.put_file(token, key, local_file)
        if err is not None:
            sys.stderr.write('%s' % err)
    return render(request, 'account/user.html', {'p': p,
                                                    'token': token,
                                                    'request': request,
                                                    'user_id': user_id,
                                                    'user': request.user,})


def teacher_signup(request):
    if request.method == 'GET':
        return render(request, 'account/teacher-signup.html', {'title': '教师注册--工大CSDN俱乐部'})
    elif request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = '%s@dlpu.edu.cn' % (email)
        if len(password1) <= 5 :
            messages.add_message(request, messages.WARNING, _(u'密码过短，至少6位'))
            return render(request, 'account/teacher-signup.html')
        if password1 == password2:
            user = User.objects.create_user(username=username, password=password1, email=email)
            u = authenticate(username=username, password=password1)
        else:
            messages.add_message(request, messages.WARNING, _(u'输入的密码不一致 !'))
            return render(request, 'account/teacher-signup.html',
                                      context_instance=RequestContext(request))
        login(request, u)
        p = Profile()
        p.user = user
        p.username = username
        p.identity = 0
        p.temp = '%s %s %s' % (username, password1, email)
        p.save()
        url = base64.encodestring(p.temp)
        send_mail(u'教师身份验证', u'尊敬的老师，点击后面的链接验证您在工大CSDN的教师身份，以便您能正常的使用作业发布等功能。'
                             u'http://dlpucsdn.com/confirm/%s' % (url),
                  'admin@dlpucsdn.com', [email])
        messages.add_message(request, messages.WARNING, _(u'已经向您的邮箱%s发送了验证邮件，请注意查收！' % (email)))
    return render(request, 'index.html',
                              context_instance=RequestContext(request))


def confirm_identity(request, t):
    s = base64.b64decode(t)
    l = re.split('\s+', s)
    username = l[0]
    password = l[1]
    u = authenticate(username=username, password=password)
    login(request, u)
    u = Profile.objects.get(username=username)
    u.identity = 2
    u.save()
    messages.add_message(request, messages.WARNING, _(u'您已认证成功，可以使用作业发布功能啦~'))
    return HttpResponseRedirect(reverse('index'))


def user_head(request):
    if request.method == 'GET':
        ret = request.GET['upload_ret']
        if ret:
            fileInfo = json.loads(base64.decodestring(ret))
            key = fileInfo['key']
            domain = 'dlpucsdn.qiniudn.com'
            base_url = qiniu.rs.make_base_url(domain, key)
            policy = qiniu.rs.GetPolicy()
            private_url = policy.make_request(base_url)  # 获得下载地址
            u = request.user
            p = Profile.objects.get(user=u)
            p.head = private_url
            p.save()
    return HttpResponseRedirect(reverse('user_profile', kwargs={'user_id': request.user.id}))


def edit_profile(request,user_id):
    return render(request, 'account/edit.html',{'request':request,
                                                   'user_id':user_id,
                                                   'user':request.user})
