from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from poster.models import *
from poster.forms import *
from django import forms    
from django.template import Context, Template
from django.contrib import auth
import operator, pusher, datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.utils.html import escape
import json
# Create your views here.

def newsfeed(request):

    posts = user_post.objects.all().order_by('-post_id__num_likes', '-post_id__created_date')
    now = datetime.datetime.now()
    new_posts = []
    for post in posts:
        if post.post_id.last_liked_date + datetime.timedelta(seconds = 30) >= now:
            post.timeleft = (post.post_id.last_liked_date - now + datetime.timedelta(seconds=30)).seconds
            new_posts.append(post)

    return render(
        request,
        'newsfeed.html',
        {'user_posts': new_posts}
    )

def timefeed(request):

    posts = user_post.objects.all().order_by('-post_id__created_date')
    now = datetime.datetime.now()
    new_posts = []
    for post in posts:
        if post.post_id.last_liked_date + datetime.timedelta(seconds = 30) >= now:
            post.timeleft = (post.post_id.last_liked_date - now + datetime.timedelta(seconds=30)).seconds
            new_posts.append(post)

    return render(
        request,
        'timefeed.html',
        {'user_posts': new_posts}
    )

def singlepost(request, id):
    current_post = get_object_or_404(user_post, pk=id)

    #navbar
    all_posts=user_post.objects.filter(post_id__data_type = 1).order_by('-post_id__num_likes')

    prev_posts_list = []
    next_post_lists = []
    current = 0
    prev_post = []
    next_post = []
    final_nav_list = []


    for i in range(len(all_posts)):
        if all_posts[i] == current_post:
            print i
            current = i
            if i > 0:
                prev_post = (all_posts[i - 1]).id
                prev_posts_list = [all_posts[i-1]]

                if i > 1:
                    prev_posts_list = [all_posts[i-2]] + prev_posts_list

                if i > 2:
                    prev_posts_list = [all_posts[i-3]] + prev_posts_list
            else:
                prev_post = (all_posts[0]).id
                prev_posts_list = []

            if i < (len(all_posts) - 1):
                next_post = (all_posts[i + 1]).id
                next_post_lists = [all_posts[i+1]]

                if i < (len(all_posts) - 2):
                    next_post_lists = [all_posts[i+2]] + next_post_lists

                if i < (len(all_posts) - 3):
                    next_post_lists = [all_posts[i+3]] + next_post_lists

            else:
                next_post = (all_posts[len(all_posts) - 1]).id
                next_post_lists = []

            break

    if all_posts:
        final_nav_list = prev_posts_list + [all_posts[current]] + next_post_lists

    return render(
        request,
        'post.html',
        {'current_post': current_post, 'prev_post': prev_post, 'next_post': next_post, 'navposts': final_nav_list}
    )

@login_required(login_url='/login/')
def upload(request):
    if request.user.has_perm('poster.add_post'):
        #Handle file upload
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():

                for things in form:
                    things = escape(things)


                if form.cleaned_data['post_image']:

                    new_post = Post(title=form.cleaned_data['title'],
                                    description=form.cleaned_data['description'],
                                    image=request.FILES['post_image'],
                                    data_type=1,
                                    created_date=datetime.datetime.now(),
                                    modified_date=datetime.datetime.now(),
                                    last_liked_date=datetime.datetime.now(),
                                    num_likes=0
                                    )

                else:
                    new_post = Post(title=form.cleaned_data['title'],
                                    description=form.cleaned_data['description'],
                                    data_type=0,
                                    created_date=datetime.datetime.now(),
                                    modified_date=datetime.datetime.now(),
                                    last_liked_date=datetime.datetime.now(),
                                    num_likes=0
                                    )

                                
                new_post.save()

                new_user_post = user_post(permission = 2, user_id = request.user, post_id = new_post)
                new_user_post.save()

                p = pusher.Pusher(
                    app_id='113826',
                    key='5a491f6fa070d42a9281',
                    secret='25ec76e5b303bfb64c80'
                )

                if new_user_post.post_id.data_type == 1:
                    # with image
                    p['new_posts'].trigger('post_event', {'title': str(new_user_post.post_id.title),
                                                    'id': new_user_post.id, 
                                                    'user': str(new_user_post.user_id), 
                                                    'post_id': new_user_post.post_id.id,
                                                    'type': new_user_post.post_id.data_type, 
                                                    'image': str(new_user_post.post_id.image), 
                                                    'description': new_user_post.post_id.description,
                                                    'created_date': new_user_post.post_id.created_date.strftime("%B %d %Y %H:%M %p"),
                                                    'modified_date': new_user_post.post_id.modified_date.strftime("%B %d %Y %H:%M %p"),
                                                    'last_liked_date': new_user_post.post_id.last_liked_date.strftime("%B %d %Y %H:%M %p"),
                                                    'num_likes': new_user_post.post_id.num_likes})
                else:
                    p['new_posts'].trigger('post_event', {'title': str(new_user_post.post_id.title), 
                                                    'id': new_user_post.id,
                                                    'post_id': new_user_post.post_id.id,
                                                    'user': str(new_user_post.user_id), 
                                                    'type': new_user_post.post_id.data_type, 
                                                    'description': new_user_post.post_id.description,
                                                    'created_date': new_user_post.post_id.created_date.strftime("%B %d %Y %H:%M %p"),
                                                    'modified_date': new_user_post.post_id.modified_date.strftime("%B %d %Y %H:%M %p"),
                                                    'last_liked_date': new_user_post.post_id.last_liked_date.strftime("%B %d %Y %H:%M %p"),
                                                    'num_likes': new_user_post.post_id.num_likes})


                return HttpResponseRedirect("/")
            else:
                messages.info(request, 'Invalid post.')
                return HttpResponseRedirect("/upload")

        else:

            # Do something for authenticated users.
            form = PostForm()
            users = User.objects.all()

            return render(request, 'upload.html', {'form': form, 'users': users})
    else:
        messages.info(request, 'You dont have the necessary permission.')
        return HttpResponseRedirect("/")        



def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Redirect to a success page.
            print request
            return HttpResponseRedirect("/")
        else:
            # Show an error page
            messages.info(request, 'Login/authentication error.')
            return HttpResponseRedirect("/login/")

    else:
        if request.user.is_authenticated():
            messages.info(request, 'You are already logged in.')
            return HttpResponseRedirect("/")

        else:
            form = LoginForm()
            return render(request, 'login.html', {'form': form})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            poster_bool = form.cleaned_data['poster_bool']

            new_user = User.objects.create_user(username, email, password)
            if poster_bool == True:
                g = Group.objects.get(name="poster")
                g.user_set.add(new_user)
            new_user.save()
        else:
            messages.info(request, 'Your signup form is invalid.')
            return HttpResponseRedirect("/signup")
        
        messages.info(request, 'Your account has been created.')
        return HttpResponseRedirect("/login")
    else:
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})

@login_required(login_url='/login/')
def like(request):

    if request.method == 'POST':
        user = request.user
        id = request.POST.get('id', '')
        post = get_object_or_404(Post, id=id)

        liked, created = Like.objects.get_or_create(post=post, user=user)

        
        p = pusher.Pusher(
                    app_id='113826',
                    key='5a491f6fa070d42a9281',
                    secret='25ec76e5b303bfb64c80'
            )

        if created == True:
            now = datetime.datetime.now()
            if post.last_liked_date + datetime.timedelta(seconds = 30) > now:
                post.num_likes += 1
                post.last_liked_date = datetime.datetime.now()
                post.save()


                p['likes'].trigger('like_event', {'post_id': post.id})
                

        return HttpResponse('')

    else:
        return HttpResponseRedirect('/')

