from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import BlogPost


# Create your views here.

def post_list(request):
    object_list = BlogPost.objects.filter(draft=False).order_by('-created_at')
    query = request.GET.get("q")
    if query:
        object_list = object_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).distinct()
    paginator = Paginator(object_list, 9)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    context = {
        'object_list': queryset,
    }

    return render(request, 'blog/list.html', context)



def post_detail(request, slug=None):
    instance = get_object_or_404(BlogPost, slug=slug)
    context = {
        'instance': instance
    }

    return render(request, 'blog/detail.html', context)





