from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from openrobots.models import *

from openrobots.api.serializers import RobotsActionPostSerializer
from openrobots.api.utils.api_functions import *

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
        if  not 'StartRunTime' in request.data:
            request.data['StartRunTime'] = ''
        if not 'FinishRunTime' in request.data:
            request.data['FinishRunTime'] = ''
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            request.data['ipaddress'] = x_forwarded_for.split(',')[0]
        else:
            request.data['ipaddress'] = request.META.get('REMOTE_ADDR')
        request.data['StartRunTime'], request.data['FinishRunTime'] = convert_to_date_format(request.data['StartRunTime'], request.data['FinishRunTime'])
        serializer = RobotsActionPostSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        robot_action_obj = serializer.save()
        robot_station = get_robot_station(request.data['RobotID'])
        if robot_station :
            robot_action_obj.update_robot_station(robot_station)
        if 'parameters' in request.data :
            if  store_and_find_changes_parameter_values(request.data['parameters'], robot_action_obj):
                robot_action_obj.update_modified_parameters(True)
                return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status = status.HTTP_204_NO_CONTENT)


    else:
        return Response(serializer.errors, status = status.HTTP_404_NOT_FOUND)
