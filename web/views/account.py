from django.shortcuts import render,redirect
from django import forms
from web import models
from web.forms import LoginForm



def login(request):
    if request.method=='GET':
        form=LoginForm()
        return render(request, 'login.html', {'form': form})
    form=LoginForm(data=request.POST)

    #1.校验数据是否为空
    if not form.is_valid():
        return render(request, 'login.html', {'form': form})

    #2.数据库获取用户信息
    user_object=models.UserInfo.objects.filter(**form.cleaned_data).first()
    if not user_object:
        return render(request, 'login.html', {'form':form, 'error': '用户名或密码错误'})

    #3.登录成功，用户信息存储session
    request.session['user_info']={'id':user_object.id,'username':user_object.username,'role':user_object.role}
    return redirect('/home/')




def logout(request):
    request.session.clear()
    return redirect('/home/')




def home(request):
    return render(request, 'home.html')