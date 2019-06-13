from django.shortcuts import render
from learning_users.models import UserProfileInfo
from .forms import UserProfileInfoForm,UserForm

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout


# Create your views here.


def index(request):
    return render(request,'learning_users/index.html')

def register(request):
    registered=False

    if request.method=='POST':
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save() #saving form data to db
            user.set_password(user.password) #hashing the save password
            user.save() #saving the hashed password

            profile=profile_form.save(commit=False) #does not commit to db yet
            profile.user=user

            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']

            profile.save()

            registered=True
        else:
            print((user_form.errors,profile_form.errors))

    else:
        user_form = UserForm(None)
        profile_form = UserProfileInfoForm(None)

    return render(request,'learning_users/registration.html',{'user_form':user_form,
                                                             'profile_form':profile_form,
                                                             'registered':registered
                                                             })

def user_login(request):

    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('learning_users:index'))
            else:
                return HttpResponse('Account not active')

        else:
            print('Someoen tried to login and failed')
            print('Username {} and password {}'.format(username,password))
            return HttpResponse('Invalid login detail supplied!')
    else:
        return render(request,'learning_users/login.html')


@login_required #decorator that make sure this view is called only if user is logged in
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('learning_users:index'))

@login_required
def special(request):
    return HttpResponse('You are logged in !.')