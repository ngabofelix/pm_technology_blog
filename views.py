from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.models import Group 
from django.contrib import messages
from django.core.files.storage import default_storage

from users.decorators import allowed_users

from .models import Posts,Topics
from .forms import PostCreationForm

import pyrebase
import os

#firebase configuration
config = {
    "apiKey": "AIzaSyC5OojanPFpSlR81Bv2AAx0ufZqvh3GQIU",
    "authDomain": "sharp-edge-745c1.firebaseapp.com",
    "projectId": "sharp-edge-745c1",
    "storageBucket": "sharp-edge-745c1.appspot.com",
    "messagingSenderId": "258934083259",
    "appId": "1:258934083259:web:a34c07655b6275bca6639e",
    "measurementId": "G-6MK7202T7L",
    "databaseURL" : "",
    
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

# Create your views here.
def home_view(request):
    tips_topic = Topics.objects.get(name='Tips')
    
    posts = Posts.objects.filter(published = True).order_by('-created_at').exclude(post_topic = tips_topic.id)
   
    high_views_posts = Posts.objects.filter(published = True).order_by('-views').exclude(post_topic = tips_topic.id)
    
    topics = Topics.objects.all().exclude(name = 'Tips')
    
    all_published_posts = Posts.objects.filter(published = True).order_by('-created_at')
    tips = Topics.objects.get(name = 'Tips')
    tips_posts = all_published_posts.filter(post_topic = tips)

    paginator = Paginator(posts,6)
    pag_number = request.GET.get('page')
    page_obj = paginator.get_page(pag_number)
    context = {
        'tips_posts':tips_posts,
        'topics':topics,
        'page_obj':page_obj,
        'high_views_posts':high_views_posts,
    }
    return render(request, 'posts/home.html',context)

def post_topic(request, pk):
    topics = Topics.objects.all()
    topic = Topics.objects.get(id=pk)
    posts = Posts.objects.filter(published=True).order_by('-created_at')
    filtered_posts = posts.filter(post_topic=topic).order_by('-created_at')
    paginator = Paginator(filtered_posts,6)
    pag_number = request.GET.get('page')
    page_obj = paginator.get_page(pag_number)
    context = {
        'page_obj':page_obj,
        'posts':posts,
        'topics':topics
    }
    return render(request, 'posts/post-topic.html', context)

def post_detail(request, slug):
    post = Posts.objects.get(slug=slug)
    post.views = post.views+1
    post.save()
    posts = Posts.objects.filter(published=True)
    topics = Topics.objects.all()
    context = {
        'post' : post,
        'posts': posts,
        'topics':topics
    }  
    return render(request, 'posts/detail.html',context)


@login_required(login_url= 'user_login')
@allowed_users(allowed_roles = ['admin','authors'])
def post_creation(request):
    if request.method == 'POST':
        form = PostCreationForm(request.POST)
        file = request.FILES['image']

        

        if form.is_valid():
            post_title = form.cleaned_data.get('title')

            file_save = default_storage.save(file.name, file)

            storage.child("files/" + file.name).put( 'static/images/' + file.name)

            delete = default_storage.delete(file.name)

            imageURL = storage.child("files/" + file.name).get_url(None)

            instance = form.save(commit = False)
            instance.author = request.user
            instance.image = imageURL
            instance.save()
            messages.success(request, 'Post with this title' + ' "'+ post_title + '" ' + 'was created successifully')
            return redirect('home')
    else:
        form = PostCreationForm()
        
    return render(request, 'posts/create.html',{'form':form})


# firebase = pyrebase.initialize_app(config)
# storage = firebase.storage()
# storage.child(PATH/DIRECTORY_ON_CLOUD).put(PATH_TO_LOCAL_IMAGE  )

# # Example (same directory, same file name)
# storage.child("images/example.jpg").put("example.jpg")

# # Example (different directory, different file name)
# storage.child("images/renamed_img.jpg").put("media/original_img.jpg")