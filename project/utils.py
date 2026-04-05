from django.db.models import Q
from .models import Tags, Project
from django.core.paginator import Paginator , PageNotAnInteger ,EmptyPage

def search_project(request):
    search_query = ""
    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    tags = Tags.objects.filter(name__icontains=search_query)

    projects_name = Project.objects.distinct().filter(
        Q(title__icontains=search_query)
        | Q(description__icontains=search_query)
        | Q(owner__name__contains=search_query)
        | Q(tags__in=tags)
    )

    page = request.GET.get("page")
    results = 9
    paginator = Paginator(projects_name, results)

    try:
        projects_name = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects_name = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects_name = paginator.page(page)

    left_index = (int(page) - 4)

    if left_index < 1:
        left_index = 1;

    right_index = (int(page) + 5)

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages

    custom_range = range(left_index, right_index + 1)

    return projects_name, search_query , custom_range ,paginator


