from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView, CreateView,DetailView
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm

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