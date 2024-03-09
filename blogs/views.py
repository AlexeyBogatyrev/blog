from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import BlogPost
from .forms import BlogPostForm


def index(request):
    """Домашняя страница приложения Learning Log"""
    return render(request, 'blogs/index.html')


@login_required
def blogposts(request):
    """Выводит список тем."""
    blogposts = BlogPost.objects.filter(
        owner=request.user).order_by('date_added')
    context = {'blogposts': blogposts}
    return render(request, 'blogs/blogposts.html', context)


@login_required
def new_blogpost(request):
    """Определяет новую тему."""
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = BlogPostForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = BlogPostForm(data=request.POST)
        if form.is_valid():
            new_blogpost = form.save(commit=False)
            new_blogpost.owner = request.user
            new_blogpost.save()

            return redirect('blogs:blogposts')
    # Вывести пустую или недействительную форму.
    context = {'form': form}
    return render(request, 'blogs/new_blogpost.html', context)


@login_required
def edit_blogpost(request, blogpost_id):
    blogpost = BlogPost.objects.get(id=blogpost_id)
    if blogpost.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = BlogPostForm(instance=blogpost)
    else:
        form = BlogPostForm(instance=blogpost, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:blogposts')
    context = {'blogpost': blogpost, 'form': form}
    return render(request, 'blogs/edit_task.html', context)
