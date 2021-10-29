from functools import reduce
from operator import and_

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import generic

from .forms import PostForm
from .models import Category, Post


class IndexView(generic.View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by('-id')
        return render(request, 'app/index.html', {
            'post_data': post_data
        })


class PostDetailView(generic.View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/post_detail.html', {
            'post_data': post_data
        })


class CreatePostView(generic.View):
    def get(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)
        return render(request, 'app/post_form.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)
        if form.is_valid():
            post_data = Post()
            post_data.author = request.user
            post_data.title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            category_data = Category.objects.get(name=category)
            post_data.category = category_data
            post_data.content = form.cleaned_data['content']
            if request.FILES:
                post_data.image = request.FILES.get('image')
            post_data.save()
            return redirect('post_detail', pk=post_data.pk)
        return render(request, 'app/post_form.html', {
            'form': form
        })


class PostEditView(generic.View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        form = PostForm(
            request.POST or None,
            initial={
                'title': post_data.title,
                'category': post_data.category,
                'content': post_data.content,
                'image': post_data.image,
            }
        )
        return render(request, 'app/post_form.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)
        if form.is_valid():
            post_data = Post.objects.get(id=self.kwargs['pk'])
            post_data.title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            category_data = Category.objects.get(name=category)
            post_data.category = category_data
            post_data.content = form.cleaned_data['content']
            if request.FILES:
                post_data.image = request.FILES.get('image')
            post_data.save()
            return redirect('post_detail', pk=post_data.pk)
        return render(request, 'app/post_form.html', {
            'form': form
        })


class PostDeleteView(generic.View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/post_delete.html', {
            'post_data': post_data
        })

    def post(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        post_data.delete()
        return redirect('index')


class CategoryView(generic.View):
    def get(self, request, *args, **kwargs):
        category_data = Category.objects.get(name=self.kwargs['category'])
        post_data = Post.objects.order_by('-id').filter(category=category_data)
        return render(request, 'app/index.html', {
            'post_data': post_data
        })


class SearchView(generic.View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by('-id')
        kw = request.GET.get('keyword')

        if kw:
            exclusion_list = set([' ', '　'])
            query_list = ''
            for word in kw:
                if not word in exclusion_list:
                    query_list += word
            query = reduce(
                and_, [Q(title__icontains=q) | Q(content__icontains=q) for q in query_list]
            )
            post_data = post_data.filter(query)
        return render(request, 'app/index.html', {
            'keyword': kw,
            'post_data': post_data
        })