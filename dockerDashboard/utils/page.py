# -*- coding: UTF-8 -*-
from django.core.paginator import Paginator


def pagination(request, queryset, display_amount=10, after_range_num=5, bevor_range_num=4):
    paginator = Paginator(queryset, display_amount)
    try:
        page = request.GET.get('page')
        if not page:
            page = 1
        else:
            page = int(page)
    except:
        page = 1
    try:
        objects = paginator.page(page)
    except Exception:
        objects = paginator.page(paginator.num_pages)
    except:
        objects = paginator.page(1)
    
    page = objects.number
    
    if page >= after_range_num:
        page_range = paginator.page_range[page - after_range_num:page + bevor_range_num]
    else:
        page_range = paginator.page_range[0:page + bevor_range_num]
    return objects, page_range , display_amount*(objects.number - 1)
