from django.shortcuts import render
from django.views.generic import ListView, CreateView,DetailView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class PostList(ListView):
    model = Post
    
class PostCreate(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content',]

class PostDetail(DetailView):
    model = Post