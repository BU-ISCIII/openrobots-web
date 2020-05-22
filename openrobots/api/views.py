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
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        serializer = RobotsActionPostSerializer(data=request.data)
        import pdb; pdb.set_trace()
        if not serializer.is_valid():
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        robot_action_obj = serializer.save()
        import pdb; pdb.set_trace()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status = status.HTTP_404_NOT_FOUND)
