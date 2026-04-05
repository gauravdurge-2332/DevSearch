def profiles(request):
    search_query = ""
    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")
        print(search_query)

    skill = Skills.objects.filter(name__iexact = search_query)

    profiles = Userprofile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_note__icontains=search_query)|
        Q(skills__in = skill)

    )
    """ So like this above line querys the data if the search Get request is posted and if not it will simply give all the profiles
    and the Q wrraper is like to search if the the request containes both name or the short not of the developer"""

    context = {"profile": profiles, "search_query": search_query}
    return render(request, "users/profile.html", context)

so like this is the view like when we hit this url with the get methode first if we dont hit it with any request it will
normal provide the all profile as we have given the empty string but now when we it hit that url with some get request we are
actually providing query to the DB now the why disticnt() as the skill =....get more than 5 skills and render the same profile
