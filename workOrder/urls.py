"""
URL configuration for workOrder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from web.views import account,tpl,my,checkout,message
from django.urls import path,re_path
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', account.login,name='login'),
    path('logout/', account.logout,name='logout'),

    path('home/', account.home,name='home'),

    path('tpl/', tpl.tpl,name='tpl'),
    path('tpl/<int:pk>/edit/', tpl.tpl_edit,name='tpl_edit'),

    path('my/', my.my,name='my'),
    path('my/add/', my.my_add,name='my_add'),
    path('my/add/plus/', my.my_add_plus,name='my_add_plus'),

    path('checkout/', checkout.checkout,name='checkout'),
    path('checkout/action/<int:action>/<int:oid>/', checkout.checkout_action,name='checkout_action'),

    path('message/', message.message,name='message'),
    path('message/mark-as-read/<int:message_id>/', message.mark_as_read, name='mark_as_read'),
    path('message/delete/<int:message_id>/', message.delete_message, name='delete_message'),


    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

]

if settings.DEBUG:  # Make sure this is set to True in your settings for development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

