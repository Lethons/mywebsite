from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
from .models import Blog, Tag

# Create your views here.
def blog_home(request):
    """ all blog list """
    ctx = {}
    blogs = Blog.objects.all()
    tags = Tag.objects.all()
    # 获取get请求，如果没有默认为1
    current_page = request.GET.get('page', 1)
    pages = Paginator(blogs, 8)  # 8个博客一页
    blogs = pages.page(current_page)  # 获取当前页的博客
    ctx['blogs'] = blogs
    ctx['tags'] = tags
    ctx['pages'] = pages
    ctx['blog_dates'] = Blog.objects.dates('publish_time', 'month', order='DESC')
    return render_to_response('blog/blog_home.html', ctx)


def blog_tag(request, blog_tag):
    """ same tag blog list """
    ctx = {}
    tag = get_object_or_404(Tag, tag=blog_tag)
    blogs = Blog.objects.filter(tag=tag)
    tags = Tag.objects.all()
    current_page = request.GET.get('page', 1)
    pages = Paginator(blogs, 2)
    blogs = pages.page(current_page)
    ctx['blogs'] = blogs
    ctx['blog_tag'] = tag
    ctx['tags'] = tags
    ctx['pages'] = pages
    ctx['blog_dates'] = Blog.objects.dates('publish_time', 'month', order='DESC')
    return render_to_response('blog/blog_tag.html', ctx)


def blog_date(request, year, month):
    """ 按日期分类 """
    ctx = {}
    blogs = Blog.objects.filter(publish_time__year=year, publish_time__month=month)
    tags = Tag.objects.all()
    # 获取get请求，如果没有默认为1
    current_page = request.GET.get('page', 1)
    pages = Paginator(blogs, 8)  # 8个博客一页
    blogs = pages.page(current_page)  # 获取当前页的博客
    ctx['blogs'] = blogs
    ctx['tags'] = tags
    ctx['pages'] = pages
    ctx['blog_dates'] = Blog.objects.dates('publish_time', 'month', order='DESC')
    ctx['year'] = year
    ctx['month'] = month
    return render_to_response('blog/blog_date.html', ctx)


def blog_detail(request, blog_pk):
    """ blog detail """
    ctx = {}
    blog = get_object_or_404(Blog, pk=blog_pk)
    tags = Tag.objects.all()
    # get blog's next or previous blog
    pre_blog = Blog.objects.filter(publish_time__lt=blog.publish_time)
    if pre_blog .count() > 0:
        pre_blog = pre_blog[0]
    else:
        pre_blog = None
    next_blog = Blog.objects.filter(publish_time__gt=blog.publish_time)
    if next_blog .count() > 0:
        next_blog = next_blog[0]
    else:
        next_blog = None
    ctx['blog'] = blog
    ctx['tags'] = tags
    ctx['pre_blog'] = pre_blog
    ctx['next_blog'] = next_blog
    ctx['blog_dates'] = Blog.objects.dates('publish_time', 'month', order='DESC')
    return render_to_response('blog/blog_detail.html', ctx)
