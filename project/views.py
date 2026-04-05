from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.defaultfilters import title
from .utils import search_project
from .models import Project, Tags , Review
from django.db.models import Q
from .forms import ProjectForm , ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

@login_required(login_url="login-page")


def project(request, id):
    project_Obj = Project.objects.get(id=id)
    tags = project_Obj.tags.all()
    form = ReviewForm()
    votes = project_Obj.getcountvote 

    if request.method == "POST":
        reviewer = request.user.userprofile

        review, created = Review.objects.get_or_create(
            owner=reviewer,
            project=project_Obj,
            defaults={
                "value": request.POST.get("value"),
                "body": request.POST.get("body"),
            }
        )

        if not created:
            messages.error(request, "You have already reviewed this project.")
        else:
            messages.success(request, "Review submitted successfully.")

        return redirect("project_det", id=project_Obj.id)


    return render(
        request,
        "project/single-project.html",
        {
            "project": project_Obj,
            "tags": tags,
            "form": form,
            "votes" : votes 
        },
    )



def homepage(request):
    projects_name, search_query,custom_range,paginator = search_project(request)


    context = {"projects": projects_name, "search_query": search_query , 'paginator':paginator , 'custom_range' : custom_range}
    return render(request, "project/project.html", context)


@login_required(login_url="login-page")
def project_creation(request):
    profile = request.user.userprofile
    form = ProjectForm()



    if request.method == "POST":

        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():

            project = form.save(commit=False)
            project.owner = profile
            project.save()

            newtags = request.POST.get('newtags').split(" ") 
            for tags in newtags:
                tags , created = Tags.objects.get_or_create(name = tags) 
                project.tags.add(tags)
            messages.success(request, "Project was created successfully...")
            return redirect("account")

    context = {"form": form}
    return render(request, "project/project_form.html", context)


@login_required(login_url="login-page")
def update_creation(request, pk):
    profile = request.user.userprofile
    project = profile.project_set.get(id=pk)

    if request.method == "GET" and "delete_tag" in request.GET:
        tag_id = request.GET.get("delete_tag")
        try:
            tag_to_delete = project.tags.get(id=tag_id)
            project.tags.remove(tag_to_delete)
        except:
            pass
        return redirect("update_project", pk=project.id)

    form = ProjectForm(instance=project)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)

        tags = project.tags.all() 
        print(tags)

        print("Data" , request.POST)
        
        if form.is_valid():
            project = form.save()
            newtags = request.POST.get('newtags').split(" ") 
            for tags in newtags:
                tags , created = Tags.objects.get_or_create(name = tags) 
                project.tags.add(tags)
            messages.success(request, "Project was updated successfully...")
            return redirect("account")

    context = {"form": form , "project":project}
    return render(request, "project/project_form.html", context)


@login_required(login_url="login-page")
def delete_creation(request, pk):
    profile = request.user.userprofile
    project = profile.project_set.get(id=pk)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project was deleted successfully...")
        return redirect("account")

    context = {"project": project}

    return render(request, "project/delete_template.html", context)

@login_required(login_url="login-page")
def allProjectsMade(request):
        profile = request.user.userprofile
        all_projects = profile.project_set.all()
        context = {"all_projects" : all_projects , "profile" : profile
                   }

        return render(request , "project/allPJ.html",context)


