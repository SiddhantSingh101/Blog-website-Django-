from django.shortcuts import render
from django.http import HttpResponse

posts = [
    {
        'author':'soddo',
        'title':'blog post',
        'content':'first post on here',
        'date':'april 22nd 2026'
    },
     {
        'author':'soddoi',
        'title':'blog post',
        'content':'second post on here',
        'date':'april 22nd 2026'
    }
    ]


def home(request):
    context = {
        'posts' : posts
    }
    return render(request ,'blog/home.html',context)
def about(request):
    return render(request ,'blog/about.html')


# Create your views here.