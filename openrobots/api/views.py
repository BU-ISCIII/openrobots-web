from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from openrobots.models import *

from openrobots.api.serializers import RobotsActionPostSerializer
from openrobots.api.utils.api_functions import *
from django.http import QueryDict

@api_view(['GET',])
def api_usage(request):

    return Response(status = status.HTTP_201_CREATED)



@api_view(['POST',])
def api_create_usage(request):
    if request.method == 'POST':
        data = request.data
        if isinstance(data, QueryDict ):
            data = data.dict()

        if  not 'StartRunTime' in data:
            data['StartRunTime'] = ''
        if not 'FinishRunTime' in data:
            data['FinishRunTime'] = ''

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            data['ipaddress'] = x_forwarded_for.split(',')[0]
        else:
            data['ipaddress'] = request.META.get('REMOTE_ADDR')
        data['StartRunTime'], data['FinishRunTime'] = convert_to_date_format(data['StartRunTime'], data['FinishRunTime'])

        serializer = RobotsActionPostSerializer(data = data)

        if not serializer.is_valid():
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        robot_action_obj = serializer.save()
        # get the station type
        robot_station = get_robot_station_type(data['RobotID'])
        if robot_station :
            robot_action_obj.update_robot_station_type(robot_station)
        # get the owner of the protocol
        protocol_owner = get_owner_of_protocol(robot_action_obj.get_protocol_id())
        robot_action_obj.update_protocol_owner(protocol_owner)
        
        if 'parameters' in data :
            if isinstance(data['parameters'], dict) :
                if  store_and_find_changes_parameter_values(data['parameters'], robot_action_obj):
                    robot_action_obj.update_modified_parameters(True)
                    return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
                else:
                    return Response(serializer.data, status = status.HTTP_201_CREATED)
            else:
                robot_action_obj.update_modified_parameters(True)
                return Response(serializer.data, status = status.HTTP_204_NO_CONTENT)
        else:
            robot_action_obj.update_modified_parameters(True)
            return Response(serializer.data, status = status.HTTP_204_NO_CONTENT)

    else:
        return Response(serializer.errors, status = status.HTTP_404_NOT_FOUND)
