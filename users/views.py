from re import search
from .utils import search_profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.autoreload import restart_with_reloader
from django.db.models import Q
from .models import Userprofile, Skills , Message
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm , MessageForm
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.


def loginUser(request):
    """Django attaches the previous user to the request"""

    if request.user.is_authenticated:
        return redirect("userProfile", id=request.user.id)

    if request.method == "POST":
        username = request.POST.get("username").strip()

        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "The user doesnt exist")

        user = authenticate(request, username=username, password=password)
        """this will query the data base and check for the username and also check the password connected to it 
        if it exist it returns the instance of that user otherwise none"""

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'temp')
        else:
            messages.error(request, "Username or Password is Wrong")

    return render(request, "users/loginPage.html", {"page": "login"})


def logoutuser(request):
    logout(request)
    messages.success(request, "Logged out successfully!!")
    """deletes the sessionid"""
    return redirect("temp")


def registerpage(request):
    form = CustomUserCreationForm()

    if request.method == "POST":
        print(request.POST)

        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            
            # Send Welcome Email
            try:
                
                send_mail(
                    "Welcome to Devsearch",
                    "Devsearch is a platform where developers meet and grow together. "
                    "We hope you enjoy being here and stay motivated to build for society.",
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print("EMAIL ERROR:", e)

            messages.success(request, "User Account Created Successfully!")

            login(request, user)
            return redirect("editaccount")

    context = {"form": form, "page": "register"}

    return render(request, "users/loginPage.html", context)


def profiles(request):

    profiles, search_query , custom_range = search_profile(request)

    context = {"profile": profiles, "search_query": search_query , 'custom_range':custom_range}
    return render(request, "users/profile.html", context)


def userProfile(request, id):
    user_details = Userprofile.objects.get(id=id)

    topSkill = user_details.skills_set.exclude(Description__exact="")
    otherskill = user_details.skills_set.filter(Description="")
    context = {
        "userprofile": user_details,
        "topskills": topSkill,
        "otherskills": otherskill,
    }
    return render(request, "users/userProfile.html", context)


@login_required(login_url="login-page")
def useraccount(request):
    profile = request.user.userprofile

    skills = profile.skills_set.all()
    project = profile.project_set.all()

    context = {
        "profile": profile,
        "skills": skills,
        "project": project,
    }
    return render(request, "users/account.html", context)


@login_required(login_url="login-page")
def editprofile(request):
    profile = request.user.userprofile
    form = ProfileForm(instance=profile)
    context = {"form": form}
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        print(form)
        if form.is_valid():
            form.save()

            return redirect("account")

    return render(request, "users/profile_form.html", context)


@login_required(login_url="login-page")
def createskills(request):
    profile = request.user.userprofile
    form = SkillForm()
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "New skill Added")

            return redirect("account")

    context = {"form": form}

    return render(request, "users/skill.html", context)


@login_required(login_url="login-page")
def updateskills(request, pk):
    profile = request.user.userprofile
    skill = profile.skills_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill updated")
            return redirect("account")

    context = {"form": form}

    return render(request, "users/skill.html", context)


@login_required(login_url="login-page")
def deleteskill(request, pk):
    profile = request.user.userprofile
    skill = profile.skills_set.get(id=pk)
    context = {
        "object": skill.name,
    }
    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill was deleted")
        return redirect("account")

    return render(request, "users/delete_skill.html", context)


@login_required(login_url="login-page")
def inbox(request):
   
    
    messages = Message.objects.filter(recipent =request.user.userprofile)
    messages_count = messages.filter(is_read = False).count() 

    context = {'message':messages , 'count' : messages_count }



    return render(request,"users/inbox.html",context=context)

@login_required(login_url="login-page")
def singleMessage(request , pk):
    message_details = Message.objects.get(id = pk)
    if message_details.is_read == False:
            message_details.is_read = True 
            message_details.save()
    context = {'message' : message_details }
    return render(request , "users/message.html", context)


@login_required(login_url="login-page")
def message_write(request,pk):
    form = MessageForm() 
    sender = request.user.userprofile 
    recepient_ = Userprofile.objects.get(id=pk) 
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid() :
            messageObject = form.save(commit=False)
            messageObject.sender = sender 
            messageObject.recipent =  recepient_

            messageObject.save()
            messages.success(request, "Message Sent")
            return redirect("userProfile", id=pk)

   
    context = {'form' : form , 'sender':sender ,}
    return render(request , "users/message_form.html" , context)
