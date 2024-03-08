from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required
from django.conf import settings
import boto3, random, string
from . import spotify_data
from .constants import *
from .models import *
from .forms import AddProfileForm, ProfileForm


# Create your views here.

def home(request):
    
    if request.method == 'GET':
        
        if 'loaded_items' in request.GET:
            
            loaded_items = request.GET['loaded_items']
            
            items = PostData.objects.all().order_by('-created_at')[int(loaded_items):int(loaded_items) + 100]
            
            return JsonResponse({ 'response': items })
        
        items = PostData.objects.all().order_by('-created_at')[:100]
        
        return render(request, 'SNS/home.html', { 
            'items': items, 
        })


def song(request, track_id):
    
    if request.method == 'GET':
        
        response = spotify_data.search_track_id(track_id)
        
        if response['status']['once'] == True:
            
            follow = MusicFollowData.objects.filter(user_id=request.user.id, music_id=track_id).exists()
            
            followers = MusicFollowData.objects.filter(music_id=track_id).count()
            
            posts_data = PostData.objects.all().filter(music_id=track_id).order_by('-created_at')
            
            posts = []
            
            for post in posts_data:
                
                replies_data = PostData.objects.all().filter(original_post_id=post.id).order_by('-created_at')
                
                replies = []
                
                for reply in replies_data:
                    
                    user = User.objects.get(id=reply.user_id)
                    
                    replies.append({
                        'user_icon': ProfileData.objects.get(user_id=reply.user_id).icon,
                        'username': user.username,
                        'date': reply.created_at,
                        'text': reply.contents,
                    })
                
                user = User.objects.get(id=post.user_id)
                
                posts.append({
                    'user_icon': ProfileData.objects.get(user_id=post.user_id).icon,
                    'username': user.username,
                    'date': post.created_at,
                    'text': post.contents,
                    'replies': replies,
                })
            
            return render(request, 'SNS/song.html', { 
                'response': response, 
                'follow': follow,
                'followers': followers,
                'posts': posts,
            })
    
    elif request.method == 'POST':
        
        follow = MusicFollowData.objects.filter(user_id=request.user.id, music_id=track_id).exists()
        
        if follow:
            MusicFollowData.objects.filter(user_id=request.user.id, music_id=track_id).delete()
        
        else:
            MusicFollowData.objects.create(
                user_id = request.user.id,
                music_id = track_id,
            )
        
        return redirect(HOST_URL + '/song/' + track_id)


def profile(request, username):
    return render(request, 'SNS/profile.html')


@login_required
def post(request):
    
    if request.method == 'GET':
        return render(request, 'SNS/post.html')
    
    elif request.method == 'POST':
        song_id = request.POST['song']
        response = spotify_data.search_track_id(song_id)
        PostData.objects.create(
            user_id = request.user.id,
            contents = request.POST['content'],
            music_id = song_id,
            song_name = response['data'][0]['song']['name'],
            artist_name = response['data'][0]['artist'][0]['name'],
            album_name = response['data'][0]['album']['name'],
            image = response['data'][0]['album']['image'],
        )
        return redirect(HOST_URL + '/home/')


def search_song(request):
    
    if request.method == 'GET':
        
        if "query" in request.GET:
        
            response = spotify_data.search_query([SPOTIFY_SEARCH_TYPE_TRACK], request.GET['query'], 20, request.GET['offset'])
        
            return JsonResponse({ 'response': response })


def username_check(request):
    
    if "username" in request.GET:
        
        username = request.GET["username"]
        
        users = User.objects.filter(username__iexact=username)
        
        if len(users) == 0:
            return JsonResponse({ 'exists': False })
        
        else:
            return JsonResponse({ 'exists': True })


def randomname(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)


def upload_file_to_s3(file):
    s3 = boto3.client('s3',
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                      region_name=settings.AWS_S3_REGION_NAME)
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    extension = file.name.split('.')[-1]
    file_name = f"{randomname(50)}.{extension}"
    s3.upload_fileobj(file, bucket_name, file_name)
    s3_link = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
    return s3_link


class  AccountRegistration(TemplateView):

    def __init__(self):
        self.params = {
        "AccountCreate":False,
        "account_form": ProfileForm(),
        "add_account_form":AddProfileForm(),
        }

    def get(self,request):
        self.params["account_form"] = ProfileForm()
        self.params["add_account_form"] = AddProfileForm()
        self.params["AccountCreate"] = False
        return render(request,"SNS/signup.html",context=self.params)
    
    def post(self,request):
        self.params["account_form"] = ProfileForm(data=request.POST)
        self.params["add_account_form"] = AddProfileForm(data=request.POST)
        if self.params["account_form"].is_valid() and self.params["add_account_form"].is_valid():
            account = self.params["account_form"].save()
            account.set_password(account.password)
            account.save()
            add_account = self.params["add_account_form"].save(commit=False)
            add_account.user = account
            if 'icon' in request.FILES:
                file = request.FILES['icon']
                s3_link = upload_file_to_s3(file)
                add_account.icon = s3_link
            add_account.save()
            self.params["AccountCreate"] = True
        else:
            print(self.params["account_form"].errors)
        return redirect(HOST_URL + '/signin/')


def Signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if "next" in request.GET:
                    next = request.GET["next"]
                    return redirect(HOST_URL + next)
                return redirect(HOST_URL + '/home/')
            else:
                return HttpResponse("アカウントが有効ではありません")
        else:
            return HttpResponse("ログインIDまたはパスワードが間違っています")
    else:
        return render(request, 'SNS/signin.html')


@login_required
def Signout(request):
    logout(request)
    return redirect(HOST_URL + '/signin/')


def csrf_token(request):
    return JsonResponse({ "token": get_token(request) })