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

    if not action in [1,2]:
        return HttpResponse("请求错误")
    ctime=datetime.datetime.now()
    if action==1:
        models.Order.objects.filter(id=oid,status=1,leader_id=request.unicom_userid).update(status=2,update_date=ctime)
    else:
        models.Order.objects.filter(id=oid, status=1, leader_id=request.unicom_userid).update(status=3,update_date=ctime)

    return redirect('/checkout/')

