from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from workspaces.models import Workspace
from api.serializers.workspace import WorkspaceSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework import status
from rest_framework.parsers import JSONParser,MultiPartParser,FormParser



@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])

def workspace_list(request):
    if request.method=="GET":
        workspaces=Workspace.objects.filter(
            Q(creator=request.user)| Q( members__user=request.user)
        ).distinct().prefetch_related("members","members__user")
        print(workspaces)
        serializer=WorkspaceSerializer(workspaces,many=True)
        return Response(serializer.data)
    elif request.method=="POST":
        serializer=WorkspaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    



        

        