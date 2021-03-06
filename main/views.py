from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Category, Post, Author
from marketing.models import Signup
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from .forms import CommentForm, PostForm


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        query = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()

    context = {
        'queryset': queryset
    }
    return render(request, 'main/search_results.html', context)


def get_category_count():
    queryset = Post.objects.values('category__title').annotate(Count('category__title'))
    return queryset


def index(request):
    featured_post = Post.objects.filter(featured=True)[:3]
    latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        news_s = Signup()
        news_s.email = email
        news_s.save()

    context = {
        'object_list' : featured_post,
        'latest': latest
    }

    return render(request, 'main/index.html', context)


def blog(request):
    category_count = get_category_count()
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 2)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    most_recent = Post.objects.order_by('-timestamp')[:3]

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'page_requested_var': page_request_var,
        'most_recent': most_recent,
        'category_count': category_count
    }
    return render(request, 'main/blog.html', context)


def post(request, id):
    category_count = get_category_count()
    post = get_object_or_404(Post, id=id)
    most_recent = Post.objects.order_by('-timestamp')[:3]

    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post", kwargs={'id': post.id}))
    
    context ={
        'post' : post,
        'most_recent': most_recent,
        'category_count': category_count,
        'form' : form,
    }
    return render(request, 'main/post.html', context)


def post_create(request):
    title = "Create"
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('post', kwargs={'id': form.instance.id }))
    context = {
        'form': form,
        'title' : title
    }
    return render(request, 'main/post_create.html', context)


def post_update(request, id):
    title = ' Update'
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('post', kwargs={'id': form.instance.id }))
    context = {
        'form': form,
        'title' : title
    }
    return render(request, 'main/post_create.html', context)


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse('post'))