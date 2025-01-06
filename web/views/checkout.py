from django.shortcuts import render,HttpResponse,redirect
from web import models
from utils.pagination import Pagination
import datetime


def checkout(request):
    count=models.Order.objects.filter(leader_id=request.unicom_userid,status=1).count()

    #1.查询自己的待审批的工单
    queryset=models.Order.objects.filter(leader_id=request.unicom_userid).order_by('status','-id')
    pager = Pagination(request, queryset.count())
    queryset = queryset[pager.start:pager.end]
    context = {
        'queryset': queryset,
        'pager_string': pager.html(),
        'count':count
    }

    return render(request, 'checkout.html', context)




def checkout_action(request,action,oid):
    # 检查操作是否合法
    if action not in [1, 2]:
        return HttpResponse("请求错误")

    ctime = datetime.datetime.now()

    # 查询指定工单
    instance = models.Order.objects.filter(id=oid, status=1, leader_id=request.unicom_userid).first()

    if not instance:
        return HttpResponse("无效的工单或权限不足")

    # 根据操作更新工单状态
    if action == 1:
        instance.status = 2  # 审批通过
    else:
        instance.status = 3  # 审批拒绝

    instance.update_date = ctime
    instance.save()

    # 获取审批结果
    result = "通过" if action == 1 else "拒绝"

    # 创建消息内容
    message_content = f"您的工单（编号：{instance.id}）已审批，结果为：{result}。"

    # 创建消息对象
    new_message = models.Message(
        sender='系统消息',
        receiver=instance.user,  # 工单发起者
        content=message_content,
        created_at=ctime,
        is_read=False  # 初始状态为未读
    )

    # 保存消息
    new_message.save()

    return redirect('/checkout/')

