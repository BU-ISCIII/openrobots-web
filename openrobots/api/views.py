from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from openrobots.models import *

from openrobots.api.serializers import RobotsActionPostSerializer

@api_view(['GET',])
def api_usage(request):

    return Response('Hola')

    try:
        pass
    except :
        return Response(status = status.HTTP_404_NOT_FOUND)

@api_view(['POST',])
def api_create_usage(request):

    if request.method == 'POST':
        import pdb; pdb.set_trace()
        serializer = RobotsActionPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            import pdb; pdb.set_trace()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_404_NOT_FOUND)
