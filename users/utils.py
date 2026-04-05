from .models import Skills, Userprofile
from django.db.models import Q
from django.core.paginator import Paginator , PageNotAnInteger ,EmptyPage



def search_profile(request):
    search_query = ""
    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")
        print(search_query)

    skill = Skills.objects.filter(name__icontains=search_query)

    profiles = Userprofile.objects.distinct().filter(
        Q(name__icontains=search_query)
        | Q(short_note__icontains=search_query)
        | Q(skills__in=skill)
    )

    page = request.GET.get("page")
    results = 6
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    left_index = (int(page) - 4)

    if left_index < 1:
        left_index = 1;

    right_index = (int(page) + 5)

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages

    custom_range = range(left_index, right_index + 1)
    return profiles, search_query , custom_range
