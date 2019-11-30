from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import requests
import dateutil.parser


def frist_home(request):


   #football-data api
    footUrl = 'https://api.football-data.org/v2/competitions/2001/scorers'
    foot = requests.get(footUrl, headers={'X-Auth-Token': '92f437c888254340bf5c2094f80cb2a5'}).json()
    footdate = dateutil.parser.parse(foot['season']['startDate'])

    #football-data PL England
    PLURL = 'https://api.football-data.org/v2/competitions/2021/scorers'
    pl = requests.get(PLURL, headers={'X-Auth-Token': '92f437c888254340bf5c2094f80cb2a5'}).json()

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
        'fd': footdate,
        'spa':spain,
        'pl': pl

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

def myPosts(request):
    context = {
        'posts': Post.objects.all(),
        'user': request.user
    }
    return render(request, 'blog/myPosts.html', context)
    
def teams(request):

    return render(request, 'blog/teams.html')
    

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

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
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
