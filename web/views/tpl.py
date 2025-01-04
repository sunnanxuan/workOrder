from django.shortcuts import render,redirect
from web import models
from utils.pagination import Pagination
from utils.bootstrap import BootStrapModelForm



class TplModelForm(BootStrapModelForm):
    class Meta:
        model=models.Template
        fields=['title','leader']


def tpl(request):
    if request.method=='GET':
        #1.创建form
        form=TplModelForm()
    else:
        form=TplModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            form=TplModelForm()

    #2.获取数据+分析
    queryset=models.Template.objects.all().order_by('-id')
    pager=Pagination(request,queryset.count())
    queryset=queryset[pager.start:pager.end]
    context={
        'queryset':queryset,
        'pager_string':pager.html(),
        'form':form
    }

    return render(request,'tpl.html',context)




def tpl_edit(request,pk):
    tpl_object=models.Template.objects.filter(id=pk).first()
    if request.method=='GET':
        form=TplModelForm(instance=tpl_object)
    else:
        form=TplModelForm(instance=tpl_object,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/tpl/')


    queryset=models.Template.objects.all().order_by('-id')
    pager=Pagination(request,queryset.count())
    queryset=queryset[pager.start:pager.end]
    context={
        'queryset':queryset,
        'pager_string':pager.html(),
        'form':form
    }

    return render(request,'tpl.html',context)



from django.http import JsonResponse

def tpl_delete(request,pk):
    try:
        models.Template.objects.filter(id=pk).delete()
        return JsonResponse({"status":True})
    except Exception as e:
        return JsonResponse({"status":False})




