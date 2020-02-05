

from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import dateutil.parser

import requests


def error_404(request, exception):
    return render(request, 'blog/404.html')


def error_500(request):
    return render(request, 'blog/500.html')




    

def frist_home(request):


   #football-data api (UEFA)
    footUrl = 'https://api.football-data.org/v2/competitions/2001/scorers'
    foot = requests.get(footUrl, headers={'X-Auth-Token': '92f437c888254340bf5c2094f80cb2a5'}).json()

    #football-data PL England
    PLURL = 'https://api.football-data.org/v2/competitions/2021/scorers'
    pl = requests.get(PLURL, headers={'X-Auth-Token': '92f437c888254340bf5c2094f80cb2a5'}).json()
    
    #football-data italy serie A
    italy = 'https://api.football-data.org/v2/competitions/2019/scorers'
    SA = requests.get(italy, headers={'X-Auth-Token': '92f437c888254340bf5c2094f80cb2a5'}).json()


    #football-data bundesliga
    ger = 'https://api.football-data.org/v2/competitions/2002/scorers'
    bun = requests.get(ger, headers={'X-Auth-Token': '92f437c888254340bf5c2094f80cb2a5'}).json()


    #football-data France Ligue 1
    fra = 'https://api.football-data.org/v2/competitions/2015/scorers'
    france = requests.get(fra, headers={'X-Auth-Token': '92f437c888254340bf5c2094f80cb2a5'}).json()

    #spain
    spainurl = 'https://api.football-data.org/v2/competitions/2014/scorers'
    spain = requests.get(spainurl, headers={'X-Auth-Token': '92f437c888254340bf5c2094f80cb2a5'}).json()
    

    # score bat api
    url = 'https://www.scorebat.com/video-api/v1/'
    bat = requests.get(url).json()
    datetime = dateutil.parser.parse(bat[0]['date'])
    
   

    context = {
        'bat': bat,
        'date': datetime,
        'foot':foot,
        'spa':spain,
        'pl': pl,
        'sa': SA,
        'fr': france,
        'bun': bun

    }

    return render(request, 'blog/first_home.html', context)


def home(request):

    context = {
        'posts': Post.objects.all(),
        'user': request.user
    }

    return render(request, 'blog/home.html', context)


def index(request):

    context = {
        'posts': Post.objects.all(),
        'user': request.user
    }
    return render(request, 'blog/index.html', context)

def posts(request):

    # Posts query-set
    posts_list = Post.objects.all().order_by("-date_posted")

    #Football highlights api
    scorebat = 'https://www.scorebat.com/video-api/v1/'
    sb = requests.get(scorebat).json()
    
    paginator = Paginator(posts_list, 15)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
        'user': request.user,
        'sb' : sb
       
    }
    return render(request, 'blog/posts.html', context)

def privacy(request):
    return render(request, 'blog/privacy.html')




class PostListView(ListView):
    model = Post
    template_name = 'blog/posts.html'
    context_object_name = 'posts'
    paginate_by = 10




class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 15

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content']
    success_url = '/posts/'
    paginate_by = 2
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/posts'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html',)
