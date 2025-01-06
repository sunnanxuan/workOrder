from django.shortcuts import render,redirect
from web import models
from utils.pagination import Pagination
from datetime import datetime
from django.http import JsonResponse
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from web.forms import MyModelForm





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
    files_paths = []
    for file in files:
        # 使用文件系统存储文件
        fs = FileSystemStorage(location=folder_path)
        file_path = fs.save(file.name, file)  # 保存文件
        relative_file_path = os.path.join(settings.MEDIA_URL, folder_name, file_path)
        files_paths.append(relative_file_path)

    # 更新实例的文件夹路径字段
    instance.files = files_paths  # 假设模型中有 files 字段
    instance.save()
    return







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


    uploaded_files = request.FILES.getlist('files')
    upload(instance, uploaded_files)  # 处理文件上传

    instance.save()

    message_content = f"有来自 {instance.user.username} 的工单尚未审批，工单编号：{instance.id}，请尽快处理。"

    # 创建 Message 对象

    new_message = models.Message(
        sender='系统消息',
        receiver=instance.leader,  # 审批人是工单的 leader
        content=message_content,
        created_at=datetime.now(),
        is_read=False  # 初始状态为未读
    )

    # 保存消息
    new_message.save()

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


