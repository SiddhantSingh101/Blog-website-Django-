from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required






def home(request):
    posts = Post.objects.all() 

    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request ,'blog/about.html')



@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  
            post.save()
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'blog/create_post.html', {'form': form})
@login_required
def profile(request):
    posts = Post.objects.filter(author=request.user) 

    context = {
        'posts': posts
    }
    return render(request, 'blog/profile.html', context)


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return redirect('home')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post) 
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = PostForm(instance=post) 

    return render(request, 'blog/edit_post.html', {'form': form})


@login_required

def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return redirect('home')

    if request.method == 'POST':
        post.delete()
        return redirect('profile')

    return render(request, 'blog/delete_post.html', {'post': post})




# Create your views here.