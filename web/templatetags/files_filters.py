import os
from django import template

register = template.Library()

@register.filter(name='basename')
def basename(value):
    """返回文件路径的文件名部分"""
    return os.path.basename(value)