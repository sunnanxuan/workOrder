from django.shortcuts import render,redirect
from web import models
from utils.pagination import Pagination
from utils.bootstrap import BootStrapModelForm
from datetime import datetime
from django.http import JsonResponse
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage



class MyModelForm(BootStrapModelForm):
    class Meta:
        model=models.Order
        fields=['tpl','desc']


def my(request):
    form=MyModelForm()
    queryset=models.Order.objects.filter(user_id=request.unicom_userid)
    pager=Pagination(request,queryset.count())
    queryset=queryset[pager.start:pager.end]
    context={
        'queryset':queryset,
        'pager_string':pager.html(),
        'form':form
    }

    return render(request,'my.html',context)



def upload(instance, files):
    # 获取存放文件的文件夹路径
    folder_name = f"{instance.id}"  # 使用订单的 id 作为文件夹名
    folder_path = os.path.join(settings.MEDIA_ROOT, folder_name)  # 例如：MEDIA_ROOT/123
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)  # 如果文件夹不存在，创建文件夹

    # 存储文件，并保存文件夹路径
    for file in files:
        # 使用文件系统存储文件
        fs = FileSystemStorage(location=folder_path)
        fs.save(file.name,file)  # 保存文件

    # 更新实例的文件夹路径字段
    instance.files= folder_path  # 假设模型中有 files_folder 字段
    instance.save()

    return folder_path  # 返






def my_add(request):
    if request.method=='GET':
        form=MyModelForm()
        return render(request,'my_add.html',{'form':form})

    form=MyModelForm(data=request.POST)

    if not form.is_valid():
        return render(request,'my_add.html',{'form':form})

    tpl_object=form.cleaned_data['tpl']
    form.instance.user_id=request.unicom_userid
    form.instance.leader_id=tpl_object.leader_id
    form.instance.create_date=datetime.now()
    instance = form.save()

    if 'files' in request.FILES:
        uploaded_files = request.FILES.getlist('files')
        upload(instance, uploaded_files)  # 处理文件上传

    instance.save()

    return redirect('/my/')





def my_add_plus(request):
    """ajax提交并创建"""
    print(request.POST)
    form=MyModelForm(data=request.POST)
    if not form.is_valid():
        return JsonResponse({'status':False,'error':form.errors})

    tpl_object=form.cleaned_data['tpl']
    form.instance.user_id = request.unicom_userid
    form.instance.leader_id = tpl_object.leader_id
    form.instance.create_date = datetime.now()
    form.save()
    return JsonResponse({'status':True})


