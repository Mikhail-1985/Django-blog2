from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.urls import reverse
from .models import *
from .utils import *
from .forms import TagForm, PostForm


def posts_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', context={'posts': posts})


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


class PostCreate(ObjectCreateMixin, View):

    form_model = PostForm
    template = 'blog/post_create.html'
    

class PostUpdete(ObjectUpdateMixin, View):

    model = Post
    form_model = PostForm
    template = 'blog/post_update_form.html'


class TagCreate(ObjectCreateMixin, View):

    form_model = TagForm
    template = 'blog/tag_create.html'


class TagUpdete(ObjectUpdateMixin, View):

    model = Tag
    form_model = TagForm
    template = 'blog/tag_update_form.html'   


class TagDelete(View):

    def get(self, request, slug):
        tag = Tag.objects.get(slug__iexact=slug)
        return render(request, 'blog/tag_delete.html', context={'tag': tag})


    def post(self, request, slug):
        tag = Tag.objects.get(slug__iexact=slug)
        tag.delete()
        return redirect(reverse('tags_list_url'))


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'
