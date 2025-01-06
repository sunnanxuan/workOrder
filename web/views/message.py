from django.shortcuts import render,redirect
from web import models
from utils.pagination import Pagination
from web.forms import MessageForm
from datetime import datetime






def message(request):
    form=MessageForm()
    queryset=models.Message.objects.filter(receiver=request.unicom_userid).order_by('-created_at')
    pager=Pagination(request,queryset.count())
    queryset=queryset[pager.start:pager.end]
    context={
        'queryset':queryset,
        'pager_string':pager.html(),
        'form':form
    }

    return render(request,'message.html',context)
