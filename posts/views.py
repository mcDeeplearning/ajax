from django.shortcuts import render,get_object_or_404, resolve_url, redirect
from django.views.generic import ListView, CreateView,DetailView
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse

# Create your views here.

class PostList(ListView):
    model = Post
    
class PostCreate(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content',]

class PostDetail(DetailView):
    model = Post
    
    def get_object(self):
        post = Post.objects.prefetch_related('comment_set__user').select_related('user')
        return get_object_or_404(post, pk=self.kwargs.get('pk'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context
        
class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content',]
    
    def form_valid(self,form):
        post = Post.objects.get(id = self.kwargs.get('pk'))
        self.object = form.save(commit=False)
        self.object.post = post
        self.object.user = self.request.user
        self.object.save()
        
        return super().form_valid(form)

# 로그인했니??
@login_required
def like(request,pk):
    if request.is_ajax():
        user = request.user
        post = Post.objects.get(pk=pk)
        
        # 사용자가 like를 눌렀으면 취소
        if post.like.filter(id=user.id).exists():
            post.like.remove(user)
        # 안눌렀으면 좋아요
        else:
            post.like.add(user)
        data = {'likes_count' : post.like.count()}
        return HttpResponse(json.dumps(data), content_type="application/json")
        
    else:
        return redirect( resolve_url('posts:detail',pk) )