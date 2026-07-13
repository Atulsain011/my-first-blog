from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Post, Comment, Category, Tag
from .forms import PostForm, CommentForm


# List of posts
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    search = request.GET.get('search', '').strip()

    if search:
        posts = posts.filter(
            Q(title__icontains=search) |
            Q(text__icontains=search) |
            Q(author__username__icontains=search) |
            Q(category__name__icontains=search) |
            Q(tags__name__icontains=search)
        ).distinct()

    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'search': search,
    })


# Post detail
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(parent=None).order_by('-created_date')
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'form': CommentForm(),
        'comments': comments,
    })


# Create new post
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


# Edit existing post
@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category)

    return render(
        request,
        "blog/post_list.html",
        {"posts": posts}
    )


def tag_posts(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag)

    return render(
        request,
        "blog/post_list.html",
        {"posts": posts}
    )


@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            parent_id = request.POST.get("parent_id")

            if parent_id:
                comment.parent = get_object_or_404(Comment, id=parent_id)

            comment.save()

    return redirect('post_detail', slug=post.slug)
