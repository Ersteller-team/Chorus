from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.middleware.csrf import get_token
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from . import spotify_data
from .constants import *
from .models import *
from .forms import AddProfileForm, ProfileForm

# Create your views here.
def home(request):
    
    response = spotify_data.search_track_id('7KYZQay4ok85FWx1e5SweU')
    
    return JsonResponse({ 'response': response })


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


def signup(request):
    
    if request.method == 'GET':
        return render(request, 'SNS/signup.html')
    
    elif request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        
        user = ProfileData(username=username, password=password, email=email)
        user.save()
        
        return JsonResponse({ 'response': 'success' })


def username_check(request):
    
    if "username" in request.GET:
        
        username = request.GET["username"]
        
        users = User.objects.filter(username__iexact=username)
        
        if len(users) == 0:
            return JsonResponse({ 'exists': False })
        
        else:
            return JsonResponse({ 'exists': True })


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

            if 'account_image' in request.FILES:
                add_account.account_image = request.FILES['account_image']

            add_account.save()

            self.params["AccountCreate"] = True

        else:
            print(self.params["account_form"].errors)

        return render(request,"SNS/signup.html",context=self.params)


def Signin(request):
    # POST
    if request.method == 'POST':
        # フォーム入力のユーザーID・パスワード取得
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Djangoの認証機能
        user = authenticate(username=username, password=password)

        # ユーザー認証
        if user:
            #ユーザーアクティベート判定
            if user.is_active:
                # ログイン
                login(request, user)
                if "next" in request.GET:
                    next = request.GET["next"]
                    return redirect(HOST_URL + next)
                return redirect('SNS/home')
            else:
                # アカウント利用不可
                return HttpResponse("アカウントが有効ではありません")
        # ユーザー認証失敗
        else:
            return HttpResponse("ログインIDまたはパスワードが間違っています")
    # GET
    else:
        return render(request, 'SNS/signin.html')


#ログアウト
@login_required
def Signout(request):
    logout(request)
    # ログイン画面遷移
    return HttpResponseRedirect(reverse('Login'))


def csrf_token(request):
    return JsonResponse({ 'token': get_token(request) })

