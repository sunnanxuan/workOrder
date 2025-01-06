from utils.bootstrap import BootStrapModelForm
from web import models
from django import forms



class LoginForm(forms.Form):
    username=forms.CharField(label="用户名",required=True)
    password=forms.CharField(label='密码',required=True,widget=forms.PasswordInput(render_value=True))

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class']='form-control'
            field.widget.attrs['placeholder'] = '请输入{}'.format(field.label)



class MyModelForm(BootStrapModelForm):
    class Meta:
        model=models.Order
        fields=['tpl','desc']



class MessageForm(BootStrapModelForm):
    class Meta:
        model=models.Message
        fields="__all__"
