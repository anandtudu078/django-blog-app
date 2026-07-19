from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Category, Comment
from .forms import CommentForm

def get_sidebar_context():
    # Helper to load common sidebar content
    categories = Category.objects.all()
    # Get 3 most recent published posts
    recent_posts = Post.objects.filter(status=1).order_by('-created_on')[:3]
    return {
        'sidebar_categories': categories,
        'recent_posts': recent_posts
    }

def post_list(request):
    posts_list = Post.objects.filter(status=1).order_by('-created_on')
    
    # Simple pagination
    paginator = Paginator(posts_list, 6) # Show 6 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        
    context = {
        'posts': posts,
        'title': 'Explore Stories & Insights',
    }
    context.update(get_sidebar_context())
    return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status=1)
    comments = post.comments.filter(active=True).order_by('created_on')
    new_comment = None
    
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            messages.success(request, 'Your comment has been submitted and is awaiting approval.')
            return redirect('post_detail', slug=post.slug)
    else:
        if request.user.is_authenticated:
            comment_form = CommentForm(initial={
                'name': request.user.username,
                'email': request.user.email
            })
        else:
            comment_form = CommentForm()
        
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    context.update(get_sidebar_context())
    return render(request, 'blog/post_detail.html', context)

def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts_list = Post.objects.filter(category=category, status=1).order_by('-created_on')
    
    paginator = Paginator(posts_list, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        
    context = {
        'posts': posts,
        'title': f'Category: {category.name}',
        'active_category': category,
    }
    context.update(get_sidebar_context())
    return render(request, 'blog/post_list.html', context)

def search_posts(request):
    query = request.GET.get('q', '')
    if query:
        posts_list = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(excerpt__icontains=query),
            status=1
        ).distinct().order_by('-created_on')
    else:
        posts_list = Post.objects.none()
        
    paginator = Paginator(posts_list, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        
    context = {
        'posts': posts,
        'title': f"Search Results for '{query}'",
        'query': query,
    }
    context.update(get_sidebar_context())
    return render(request, 'blog/post_list.html', context)


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome to the blog, {user.username}.')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'registration/register.html', context)
