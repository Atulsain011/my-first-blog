from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Post, Comment
from .forms import PostForm, CommentForm


# ─── Post List ───────────────────────────────────────────────────────────────
# Just renders the template.
# All posts are loaded by JavaScript via fetch('/api/posts/') in post_list.html.
def post_list(request):
    return render(request, 'blog/post_list.html')


# ─── Post Detail ─────────────────────────────────────────────────────────────
# Looks up the post only to get its ID and slug for the template's data-* attrs.
# Actual post content (title, text, category, tags, comments, image)
# is fetched by JavaScript via GET /api/posts/<id>/ in post_detail.html.
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})


# ─── Create Post ─────────────────────────────────────────────────────────────
# Only renders the form.
# Form submission is handled by JavaScript via POST /api/posts/ in post_edit.html.
@login_required
def post_new(request):
    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


# ─── Edit Post ───────────────────────────────────────────────────────────────
# Looks up the post only to pass its ID to the template's data-* attributes.
# Form submission is handled by JavaScript via PATCH /api/posts/<id>/ in post_edit.html.
@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'post': post})


# ─── Category Posts ──────────────────────────────────────────────────────────
# Just renders the template.
# JavaScript in post_list.html detects /category/<slug>/ in the URL and calls
# fetch('/api/posts/?category=<slug>') automatically.
def category_posts(request, slug):
    return render(request, 'blog/post_list.html')


# ─── Tag Posts ───────────────────────────────────────────────────────────────
# Just renders the template.
# JavaScript in post_list.html detects /tag/<slug>/ in the URL and calls
# fetch('/api/posts/?tag=<slug>') automatically.
def tag_posts(request, slug):
    return render(request, 'blog/post_list.html')


# ─── Add Comment ─────────────────────────────────────────────────────────────
# Comments still use the normal Django route (no REST API for comments yet).
# Saves the comment to the database and redirects back to the post.
@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent = get_object_or_404(Comment, id=parent_id)
                comment.parent = parent
                comment.save()

    return redirect('post_detail', slug=post.slug)
