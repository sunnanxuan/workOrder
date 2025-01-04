"""
视图函数：

from utils.pagination import Pagination
def depart_list(request):
    query = models.Department.objects.all()
    pager=Pagination(request,query.count())
    queryset=query[pager.start:pager.end]

    context={'queryset':queryset,"pager_string":pager.html()}
    return render(request,'depart_list.html',context)



前端页面：
        <ul class="pagination">
            {{ pager_string }}
        </ul>




"""






from django.utils.safestring import mark_safe
from web import models
import copy

class Pagination(object):
    def __init__(self,request,total_count):
        page = request.GET.get("page", "1")
        if not page.isdecimal():
            page=1
        else:
            page=int(page)
            if page < 1:
                page = 1

        self.page=page
        self.start = (page - 1) * 10
        self.end = page * 10

        self.total_count = total_count
        total_page_count, div = divmod(self.total_count, 10)
        if div:
            total_page_count += 1
        self.total_page_count=total_page_count

        self.query_dict=copy.deepcopy(request.GET)
        self.query_dict._mutable=True




    def html(self):
        pager_list = []

        if self.total_page_count <= 11:
            pager_start = 1
            pager_end = self.total_page_count + 1
        else:
            if self.page <= 5:
                pager_start = 1
                pager_end = 11 + 1
            elif self.page + 5 > self.total_page_count:
                pager_start = self.total_page_count - 10
                pager_end = self.total_page_count + 1
            else:
                pager_start = self.page - 5
                pager_end = self.page + 5 + 1
        for i in range(pager_start, pager_end):
            self.query_dict.setlist("page",[i])
            query=self.query_dict.urlencode()
            if i == self.page:
                element = '<li class="active"><a href="?{0}">{1}</a></li>'.format(query,i)
            else:
                element = '<li><a href="?{0}">{1}</a></li>'.format(query,i)
            pager_list.append(element)
        pager_string = mark_safe("".join(pager_list))
        return pager_string

