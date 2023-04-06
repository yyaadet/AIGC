#coding=utf-8

from django import template
import urllib.request, urllib.parse, urllib.error
import types


register = template.Library()

PAGE_NUMBER = 10


@register.inclusion_tag("tags/pagination.html", name="pagination")
def do_pagination(pager, prefix, request=None):
    if not pager:
        return {"pager":None}
    
    if prefix and prefix[-1] == "/":
        prefix = prefix[:len(prefix) - 1]
        
    cur_page = pager.number
    start = cur_page - PAGE_NUMBER
    if start <= 0:
        start = 1
    end = cur_page + PAGE_NUMBER
    if end >= pager.paginator.num_pages:
        end = pager.paginator.num_pages 
    pages = list(range(start, end+1))
    
    params = ""
    if request:
        if request.method == "GET":
            params = urlencode_utf8(request.GET)
        else:
            params = urlencode_utf8(request.POST)
    
    return {"pager":pager, "prefix":prefix, "pages":pages, "params":params}


def urlencode_utf8(params):
    new_params = {}
    for key, value in params.items():
        if key == "page":
            continue
        if isinstance(key, str):
            key = key.encode("utf-8")
        if isinstance(value, str):
            value = value.encode("utf-8")
        
        new_params[key] = value
    
    return urllib.parse.urlencode(new_params)
    