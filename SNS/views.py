from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Q
import boto3, random, string
from io import BytesIO
from PIL import Image
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
        
        latest_music_ids = PostData.objects.values('music_id').annotate(latest_created_at=models.Max('created_at'))
        items = PostData.objects.filter(created_at__in=latest_music_ids.values('latest_created_at')).order_by('created_at').reverse()[:100]
        
        return render(request, 'SNS/home.html', { 
            'items': items, 
        })


def search(request):
    
    if request.method == 'GET':
        
        return render(request, 'SNS/search.html')


def song(request, track_id):
    
    if request.method == 'GET':
        
        response = spotify_data.search_track_id(track_id)
        
        if response['status']['one'] == True:
            
            follow = MusicFollowData.objects.filter(user_id=request.user.id, music_id=track_id).exists()
            
            followers = MusicFollowData.objects.filter(music_id=track_id).count()
            
            posts_data = PostData.objects.filter(Q(music_id=track_id) & Q(original_post_id=None)).order_by('-created_at')
            
            posts = []
            
            for post in posts_data:
                
                replies_data = PostData.objects.filter(original_post_id=post.id).order_by('-created_at')
                
                replies = []
                
                for reply in replies_data:
                    
                    user = User.objects.get(id=reply.user_id)
                    
                    replies.append({
                        'id': reply.id,
                        'user_icon': ProfileData.objects.get(user_id=reply.user_id).icon,
                        'username': user.username,
                        'user_id': post.user_id,
                        'date': reply.created_at,
                        'good': GoodData.objects.filter(post_id=reply.id).count(),
                        'good_status': GoodData.objects.filter(post_id=reply.id, gooded_id=request.user.id).exists(),
                        'text': reply.contents,
                    })
                
                user = User.objects.get(id=post.user_id)
                
                posts.append({
                    'id': post.id,
                    'user_icon': ProfileData.objects.get(user_id=post.user_id).icon,
                    'username': user.username,
                    'user_id': post.user_id,
                    'date': post.created_at,
                    'good': GoodData.objects.filter(post_id=post.id).count(),
                    'good_status': GoodData.objects.filter(post_id=post.id, gooded_id=request.user.id).exists(),
                    'text': post.contents,
                    'replies': replies,
                })
            
            en_response = spotify_data.search_track_id(track_id, 'en')
            
            same_response = spotify_data.search_track_artist(SPOTIFY_SEARCH_TYPE_TRACK, en_response['data'][0]['song']['name'], en_response['data'][0]['artist'][0]['name'], 20, 0)
            
            return render(request, 'SNS/song.html', { 
                'response': response, 
                'same_response': same_response,
                'same': same_response['status']['total'] >= 2,
                'follow': follow,
                'followers': followers,
                'posts': posts,
            })
    
    elif request.method == 'POST':
        
        song = spotify_data.search_track_id(track_id)
        
        follow = MusicFollowData.objects.filter(user_id=request.user.id, music_id=track_id).exists()
        
        if follow:
            MusicFollowData.objects.filter(user_id=request.user.id, music_id=track_id).delete()
        
        else:
            MusicFollowData.objects.create(
                user_id = request.user.id,
                music_id = track_id,
                song_name = song['data'][0]['song']['name'],
                artist_name = song['data'][0]['artist'][0]['name'],
                album_name = song['data'][0]['album']['name'],
                image = song['data'][0]['album']['image'],
            )
        
        return redirect(HOST_URL + '/search/song/' + track_id)


def album(request, album_id):
    
    if request.method == 'GET':
        
        response = spotify_data.search_album_id(album_id)
        
        return render(request, 'SNS/album.html', {
            'response': response,
        })


def artist(request, artist_id):
    
    if request.method == 'GET':
        
        response = spotify_data.search_artist_id(artist_id)
        
        return render(request, 'SNS/artist.html', {
            'response': response,
        })


def playlist(request, playlist_id):
    
    if request.method == 'GET':
        
        response = spotify_data.search_public_playlist_id(playlist_id)
        
        return render(request, 'SNS/playlist.html', {
            'response': response,
        })


@login_required
def post(request):
    
    if request.method == 'GET':
        
        song_data = {
            'song': {'name': '', 'id': '', 'preview': ''},
            'artist': [{'name': '', 'id': ''}],
            'album': {'name': '', 'id': '', 'image': ''}
        }
        
        song = False
        post = None
        reply_to = None
        recent_play = { 'data': [] }
        recent = False
        
        if 'song_id' in request.GET:
            
            song_data = spotify_data.search_track_id(request.GET['song_id'])['data'][0]
            song = True
        
        else:
            
            access_token = ProfileData.objects.get(user_id=request.user.id).spotify_access_token
            
            if access_token != None:
                recent_play = spotify_data.get_recent_play(access_token, request, 50)
                recent = True
        
        if 'post_id' in request.GET:
            
            post_check = PostData.objects.get(id=request.GET['post_id'])
            if post_check.user_id == request.user.id:
                post = post_check
        
        if 'reply_to' in request.GET:
            
            reply_to = request.GET['reply_to']
        
        return render(request, 'SNS/post.html', {
            'song': song_data,
            'response': song,
            'post': post,
            'reply_to': reply_to,
            'recent_song': recent_play['data'],
            'recent': recent,
        })
    
    elif request.method == 'POST':
        song_id = request.POST['song']
        response = spotify_data.search_track_id(song_id)
        
        if 'post_id' in request.POST:
            post = PostData.objects.get(id=request.POST['post_id'])
            if post.user_id == request.user.id:
                post.contents = request.POST['content']
                post.save()
        
        else:
            if 'reply_to' in request.POST:
                reply_to = request.POST['reply_to']
            else:
                reply_to = None
            
            PostData.objects.create(
                user_id = request.user.id,
                contents = request.POST['content'],
                music_id = song_id,
                song_name = response['data'][0]['song']['name'],
                artist_name = response['data'][0]['artist'][0]['name'],
                album_name = response['data'][0]['album']['name'],
                image = response['data'][0]['album']['image'],
                original_post_id = reply_to,
            )
        
        return redirect(HOST_URL + '/search/song/' + song_id)


@login_required
def postGood(request):
    
    if request.method == 'GET':
        
        if 'status' in request.GET and 'post_id' in request.GET and 'user_id' in request.GET and 'posted_id' in request.GET:
            
            status = request.GET['status']
            post_id = request.GET['post_id']
            user_id = request.GET['user_id']
            posted_id = request.GET['posted_id']
            
            if status == 'good':
                GoodData.objects.create(
                    gooded_id = int(user_id),
                    post_id = int(post_id),
                    admin_id = int(posted_id),
                )
            else:
                GoodData.objects.filter(gooded_id=user_id, post_id=post_id).delete()
            
            count = GoodData.objects.filter(post_id=post_id).count()
            
            return JsonResponse({
                'success': True,
                'create': status == 'good',
                'count': count,
            })
        
        else:
            return JsonResponse({ 'status': 'failed' })
    
    else:
        return JsonResponse({ 'status': 'failed' })


@login_required
def postDelete(request):
    
    if request.method == 'GET':
        
        if 'user' in request.GET and 'post_id' in request.GET:
            
            user = int(request.GET['user'])
            post_id = int(request.GET['post_id'])
            
            post = PostData.objects.get(id=post_id)
            
            if post.user_id == user:
                
                post.delete()
                
                PostData.objects.filter(original_post_id=post_id).delete()
                
                goods = GoodData.objects.all()
                
                for good in goods:
                    if not PostData.objects.filter(id=good.post_id).exists():
                        good.delete()
                
                return JsonResponse({ 'success': True })
    
    return JsonResponse({ 'success': False })


@login_required
def spotify(request):
    
    user = ProfileData.objects.get(user_id=request.user.id)
    
    if user.spotify_refresh_token == None:
    
        auth_url = spotify_data.get_authenticate_url()
        
        return render(request, 'SNS/authenticate.html', {
            'auth_url': auth_url,
        })
    
    else:
        
        now_play = spotify_data.get_current_play(user.spotify_access_token, request)
        # return JsonResponse({ 'response': now_play })
        
        recent_play = spotify_data.get_recent_play(user.spotify_access_token, request, 50)
        
        library = spotify_data.get_my_library(user.spotify_access_token, request)
        # return JsonResponse({ 'response': library })
        
        return render(request, 'SNS/spotify.html', {
            'recent_play': recent_play,
            'now_play': now_play,
            'response': library,
        })


@login_required
def spotify_callback(request):
    
    if request.method == 'GET':
        
        if 'code' in request.GET:
            
            authenticate_code = request.GET['code']
            
            access_token, refresh_token = spotify_data.get_access_token_authentication(authenticate_code)
            
            user = ProfileData.objects.get(user_id=request.user.id)
            user.spotify_access_token = access_token
            user.spotify_refresh_token = refresh_token
            user.save()
    
    return redirect(HOST_URL + '/spotify')


def profile(request, username):
    
    if request.method == 'GET':
        
        user_obj = User.objects.get(username=username)
        
        song_follow = MusicFollowData.objects.filter(user_id=user_obj.id).count()
        
        user_follow = UserFollowData.objects.filter(user_id=user_obj.id).count()
        
        follower = UserFollowData.objects.filter(opponent_id=user_obj.id).count()
        
        profile = ProfileData.objects.get(user_id=user_obj.id)
        
        posts_data = PostData.objects.filter(Q(user_id=user_obj.id) & Q(original_post_id=None)).order_by('-created_at')
        
        posts = []
        
        for post in posts_data:
            
            posts.append({
                'id': post.id,
                'username': user_obj.username,
                'user_id': post.user_id,
                'date': post.created_at,
                'good': GoodData.objects.filter(post_id=post.id).count(),
                'good_status': GoodData.objects.filter(post_id=post.id, gooded_id=request.user.id).exists(),
                'text': post.contents,
                'song_id': post.music_id,
                'song': post.song_name,
                'artist': post.artist_name,
                'album': post.album_name,
                'image': post.image,
            })
        
        follow = UserFollowData.objects.filter(user_id=request.user.id, opponent_id=user_obj.id).exists()
        
        return render(request, 'SNS/profile-post.html', {
            'user_obj': user_obj,
            'profile': profile,
            'song_follow': song_follow,
            'user_follow': user_follow,
            'follow': follow,
            'follower': follower,
            'posts': posts,
        })
    
    elif request.method == 'POST':
        
        opponent = request.POST['user_id']
        status = request.POST['status']
        
        if status == 'true':
            UserFollowData.objects.filter(user_id=request.user.id, opponent_id=opponent).delete()
        
        else:
            UserFollowData.objects.create(
                user_id = request.user.id,
                opponent_id = opponent,
            )
        
        user_obj = User.objects.get(id=opponent)
        
        return redirect(HOST_URL + '/profile/' + user_obj.username)


def user_song(request, username):
    
    user_obj = User.objects.get(username=username)
    
    song_follow = MusicFollowData.objects.filter(user_id=user_obj.id).count()
    
    user_follow = UserFollowData.objects.filter(user_id=user_obj.id).count()
    
    follower = UserFollowData.objects.filter(opponent_id=user_obj.id).count()
    
    profile = ProfileData.objects.get(user_id=user_obj.id)
    
    follow = UserFollowData.objects.filter(user_id=request.user.id, opponent_id=user_obj.id).exists()
    
    response = MusicFollowData.objects.filter(user_id=user_obj.id)
    
    return render(request, 'SNS/profile-song.html', {
            'user_obj': user_obj,
            'profile': profile,
            'song_follow': song_follow,
            'user_follow': user_follow,
            'follow': follow,
            'follower': follower,
            'response': response,
        })


def user_follow(request, username):
    
    user_obj = User.objects.get(username=username)
    
    song_follow = MusicFollowData.objects.filter(user_id=user_obj.id).count()
    
    user_follow = UserFollowData.objects.filter(user_id=user_obj.id).count()
    
    follower = UserFollowData.objects.filter(opponent_id=user_obj.id).count()
    
    followed = UserFollowData.objects.filter(user_id=request.user.id)
    
    follow = UserFollowData.objects.filter(user_id=request.user.id, opponent_id=user_obj.id).exists()
    
    profile = ProfileData.objects.get(user_id=user_obj.id)
    
    no = UserFollowData.objects.filter(user_id=user_obj.id)
    
    response = []
    for i in no:
        user = User.objects.get(id=i.opponent_id)
        prof = ProfileData.objects.get(user_id=i.opponent_id)
        response.append({
            'id': i.user_id,
            'username': user.username,
            'icon': prof.icon,
        })
    
    return render(request, 'SNS/profile-user.html', {
        'response': response,
        'user_obj': user_obj,
        'profile': profile,
        'song_follow': song_follow,
        'user_follow': user_follow,
        'follower': follower,
        'username': username,
        'followed': followed,
        'follow': follow,
        'method': 'follow',
        'method_ja': 'フォロー',
    })


def user_follower(request, username):
    
    user_obj = User.objects.get(username=username)
    
    song_follow = MusicFollowData.objects.filter(user_id=user_obj.id).count()
    
    user_follow = UserFollowData.objects.filter(user_id=user_obj.id).count()
    
    follower = UserFollowData.objects.filter(opponent_id=user_obj.id).count()
    
    follow = UserFollowData.objects.filter(user_id=request.user.id, opponent_id=user_obj.id).exists()
    
    profile = ProfileData.objects.get(user_id=user_obj.id)
    
    no = UserFollowData.objects.filter(opponent_id=user_obj.id)
    
    response = []
    for i in no:
        user = User.objects.get(id=i.user_id)
        prof = ProfileData.objects.get(user_id=i.user_id)
        response.append({
            'id': i.user_id,
            'username': user.username,
            'icon': prof.icon,
        })
    return render(request, 'SNS/profile-user.html', {
        'response': response,
        'user_obj': user_obj,
        'profile': profile,
        'song_follow': song_follow,
        'user_follow': user_follow,
        'follower': follower,
        'follow': follow,
        'username': username,
        'method': 'follower',
        'method_ja': 'フォロワー',
    })


# Json Response

def search_song(request):
    
    if request.method == 'GET':
        
        if "query" in request.GET:
        
            response = spotify_data.search_query(SPOTIFY_SEARCH_TYPE_TRACK, request.GET['query'], 20, request.GET['offset'])
        
            return JsonResponse({ 'response': response })


def search_any(request):
    
    if request.method == 'GET':
        
        if "query" in request.GET:
        
            response = spotify_data.search_query(SPOTIFY_SEARCH_TYPE_ALL, request.GET['query'], 20, request.GET['offset'])
        
            return JsonResponse({ 'response': response })


def username_check(request):
    
    if "username" in request.GET:
        
        username = request.GET["username"]
        
        users = User.objects.filter(username__iexact=username)
        
        if len(users) == 0:
            return JsonResponse({ 'exists': False })
        
        else:
            return JsonResponse({ 'exists': True })


# Account

def randomname(n):
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return ''.join(randlst)


def upload_file_to_s3(file, file_name=None):
    im = Image.open(file)
    image_size = im.size
    if image_size[0] <= image_size[1]:
        min_size = image_size[0]
    else:
        min_size = image_size[1]
    im_crop = im.crop((image_size[0] / 2 - min_size / 2, image_size[1] / 2 - min_size / 2, image_size[0] / 2 + min_size / 2, image_size[1] / 2 + min_size / 2))
    im_resize = im_crop.resize((200, 200))
    s3 = boto3.client('s3',
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                      region_name=settings.AWS_S3_REGION_NAME)
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    extension = file.name.split('.')[-1]
    if file_name == None:
        file_name = f"{randomname(50)}.{extension}"
    byte_file = BytesIO()
    im_resize.save(byte_file, format='PNG')
    byte_file.seek(0)
    s3.upload_fileobj(byte_file, bucket_name, file_name)
    s3_link = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
    return s3_link


def profile_edit(request, username):
    
    if request.user.username == username:
        
        user = User.objects.get(username=username)
        prof = ProfileData.objects.get(user_id=user.id)
        
        if request.method == 'GET':
            
            return render(request, 'SNS/profile-edit.html', {
                'user_obj': user,
                'profile': prof,
            })
        
        elif request.method == 'POST':
            
            if 'icon' in request.FILES:
                file_name = None
                if prof.icon != 'https://music-sns.s3.ap-northeast-1.amazonaws.com/default.png':
                    file_name = prof.icon.split('/')[-1]
                file = request.FILES['icon']
                s3_link = upload_file_to_s3(file, file_name)
                prof.icon = s3_link
            
            prof.description = request.POST['description']
            
            prof.save()
            
            return redirect(HOST_URL + '/profile/' + username)


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
            else:
                add_account.icon = 'https://music-sns.s3.ap-northeast-1.amazonaws.com/default.png'
            add_account.spotify_access_token = None
            add_account.spotify_refresh_token = None
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