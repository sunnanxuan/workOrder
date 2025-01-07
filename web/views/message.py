from django.shortcuts import render,redirect
from web import models
from utils.pagination import Pagination
from web.forms import MessageForm
from datetime import datetime






def message(request):
    form = MessageForm()
    queryset = models.Message.objects.filter(receiver=request.unicom_userid).order_by('is_read', '-created_at')  # 按未读优先、时间倒序排序
    pager = Pagination(request, queryset.count())
    queryset = queryset[pager.start:pager.end]
    context = {
        'queryset': queryset,
        'pager_string': pager.html(),
        'form': form,
    }

    return render(request, 'message.html', context)




from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

def delete_message(request, message_id):
    # 获取消息对象
    message = get_object_or_404(models.Message, id=message_id, receiver=request.unicom_userid)

    # 删除消息
    message.delete()

    # 重定向回消息列表页面
    return HttpResponseRedirect(reverse('message'))




def mark_as_read(request, message_id):
    # 获取消息对象
    message = get_object_or_404(models.Message, id=message_id, receiver=request.unicom_userid)

    # 如果消息未读，则标记为已读
    if not message.is_read:
        message.is_read = True
        message.save()

    # 重定向回消息列表页面
    return HttpResponseRedirect(reverse('message'))

