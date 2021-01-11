from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.urls import reverse
from .models import *
from .utils import *
from .forms import TagForm, PostForm
from django.contrib.auth.mixins import LoginRequiredMixin # проверка на аутентификацию
from django.core.paginator import Paginator
from django.db.models import Q # для работы с поиском

def posts_list(request):

    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(
            Q(title__icontains=search_query) | Q(body__icontains=search_query)
        )
    else:
        posts = Post.objects.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1) # если не будет найдено, то будет подставлена 1
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    if page.has_previous() == True:
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''
    if page.has_next() == True:
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''

    context={
        'page_object': page,
        'is_paginated': is_paginated,
        'prev_url': prev_url,
        'next_url': next_url,
    }
    return render(request, 'blog/index.html', context=context)


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):

    form_model = PostForm
    template = 'blog/post_create.html'
    raise_exception = True
    

class PostUpdete(LoginRequiredMixin, ObjectUpdateMixin, View):

    model = Post
    form_model = PostForm
    template = 'blog/post_update_form.html'
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):

    model = Post
    template = 'blog/post_delete.html'
    redirect_url = 'posts_list_url'
    raise_exception = True


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):

    form_model = TagForm
    template = 'blog/tag_create.html'
    raise_exception = True


class TagUpdete(LoginRequiredMixin, ObjectUpdateMixin, View):

    model = Tag
    form_model = TagForm
    template = 'blog/tag_update_form.html'
    raise_exception = True 


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):

    model = Tag
    template = 'blog/tag_delete.html'
    redirect_url = 'tags_list_url'
    raise_exception = True


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'
