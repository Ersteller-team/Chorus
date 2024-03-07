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
    
    return render(request, 'SNS/home.html')


def song(request, track_id):
    
    if request.method == 'GET':
        
        response = spotify_data.search_track_id(track_id)
        
        if response['status']['once'] == True:
            
            return render(request, 'SNS/song.html', { 
                'response': response, 
            })
    
    elif request.method == 'POST':
        
        response = spotify_data.search_track_id(track_id)
        
        return JsonResponse({ 'response': response })

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