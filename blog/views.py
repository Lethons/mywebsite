from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
from .models import Blog, Tag


def comment_code(req, blogs):
    ctx = {}
    tags = Tag.objects.all()
    # 获取get请求，如果没有默认为1
    page_num = req.GET.get('page', 1)
    pages = Paginator(blogs, 6)  # 8个博客一页
    if int(page_num) > pages.num_pages:
        error404 = True
        page_num = 1
    else:
        error404 = False
    blogs = pages.page(page_num)  # 获取当前页的博客
    current_page_num = blogs.number  # 获取当前页码
    page_range = list(range(max(current_page_num-2, 1), min(current_page_num+2, pages.num_pages)+1))
    if page_range[0] >= 2:
        page_range.insert(0, 1)
        if page_range[1] > 2:
            page_range.insert(1, '...')
    if page_range[-1] <= pages.num_pages-1:
        page_range.append(pages.num_pages)
        if page_range[-2] < pages.num_pages-1:
            page_range.insert(-1, '...')

    ctx['blogs'] = blogs
    ctx['tags'] = tags
    ctx['pages'] = pages
    ctx['page_range'] = page_range
    ctx['blog_dates'] = Blog.objects.dates('publish_time', 'month', order='DESC')
    return ctx, error404


# Create your views here.
def blog_home(request):
    """ all blog list """
    blogs = Blog.objects.all()
    ctx, error404 = comment_code(request, blogs)
    if error404:
        return render_to_response('blog/error404.html')
    return render_to_response('blog/blog_home.html', ctx)


def blog_tag(request, blog_tag):
    """ same tag blog list """
    tag = get_object_or_404(Tag, tag=blog_tag)
    blogs = Blog.objects.filter(tag=tag)
    ctx, error404 = comment_code(request, blogs)
    ctx['blog_tag'] = tag
    if error404:
        return render_to_response('blog/error404.html')
    return render_to_response('blog/blog_tag.html', ctx)


def blog_date(request, year, month):
    """ 按日期分类 """
    blogs = Blog.objects.filter(publish_time__year=year, publish_time__month=month)
    ctx, error404 = comment_code(request, blogs)
    ctx['year'] = year
    ctx['month'] = month
    if error404:
        return render_to_response('blog/error404.html')
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
