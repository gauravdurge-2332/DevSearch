from django.http import JsonResponse
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework.response import Response
from project.models import Project , Tags , Review
from users.models import Userprofile
from .serializer import ProjectSerializers



@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET' : '/api/projects'},
        {'GET' : '/api/projects/id'},
        {'POST' : '/api/projects/id/vote'},

        {'POST' : '/api/users/token'},
        {'POST' : '/api/users/token/refresh'},



    ]

    return Response(routes)


@api_view(['GET'])

def getProjects(request):
    print("USER" , request.user)
    projects = Project.objects.all() 
    serializer = ProjectSerializers(projects , many = True)

    return Response(serializer.data)


@api_view(['GET'])
def getProject(request,pk):
    project = Project.objects.get(id=pk) 
    serializer = ProjectSerializers(project , many = False)

    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request , pk):
    project = Project.objects.get(id=pk)
    user = request.user.userprofile
    data = request.data

    review , created = Review.objects.get_or_create(
        owner=user,
        project = project,
        defaults={'value': data.get('value')}
    )

    if not created:
        review.value = data.get('value')
        review.save() 
    
    project.getcountvote
    project.save()

    serilizer = ProjectSerializers(project , many = False)

    return Response(serilizer.data)

