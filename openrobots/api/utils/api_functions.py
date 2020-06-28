from openrobots.models import *
from datetime import datetime
from openrobots.openrobots_config import *
def check_valid_date_format (date):
    '''
    Function:
        check if date has the right format
    Return:
        True/False
    '''
    try:
        datetime.strptime(date, '%Y/%m/%d %H:%M:%S')
        return True
    except:
        return False

def convert_to_date_format(start_date, finish_date):
    '''
    Function:
        convert the date into datetime object
        If start date has not a valid format it will be set to None
        If finish_date is not valid it will be set to the time now
    Inputs:
        start_date
        finish_date
    Functions:
        check_valid_date_format     # located at this file
    Return:
        formated_date
    '''
    if check_valid_date_format(start_date):
        converted_start_date = datetime.strptime(start_date, '%Y/%m/%d %H:%M:%S')
    else:
        converted_start_date = None
    if check_valid_date_format(finish_date):
        converted_finish_date = datetime.strptime(finish_date, '%Y/%m/%d %H:%M:%S')
    else:
        converted_finish_date = datetime.now()
    return converted_start_date, converted_finish_date

def get_file_mapping_obj_from_protocol_id(protocol_id):
    '''
    Function:
        The function get the file mapping object from the protocol id
    Inputs:
        protocol_id     # protocol id for getting the file mapping
    Return:
        file_mapping_obj. None if not match
    '''
    if FileIDUserRequestMapping.objects.filter(fileID__exact = protocol_id).exists():
        return FileIDUserRequestMapping.objects.filter(fileID__exact = protocol_id).last()
    return None

def get_owner_of_protocol(protocol_id) :
    '''
    Function:
        The function get the protocol id and look for the owner of the protocol
    Inputs:
        protocol_id     # protocol id to find the owner
    Return:
        usr_obj. None if not match
    '''
    if protocol_id :
        if FileIDUserRequestMapping.objects.filter(fileID__exact = protocol_id).exists():
            file_mapping = FileIDUserRequestMapping.objects.filter(fileID__exact = protocol_id).last()
            station = file_mapping.get_station()
            protocol = file_mapping.get_station_protocol()
            if station == 'Station C':
                if protocol == '1':
                    if RequestForStationC_Prot1.objects.filter(protocolID__exact = protocol_id).exists():
                        station_obj = RequestForStationC_Prot1.objects.filter(protocolID__exact = protocol_id).last()
                        return station_obj.get_user_file_obj()
                else:
                    if RequestForStationC_Prot2.objects.filter(protocolID__exact = protocol_id).exists():
                        station_obj = RequestForStationC_Prot2.objects.filter(protocolID__exact = protocol_id).last()
                        return station_obj.get_user_file_obj()
            elif station == 'Station B':
                if RequestForStationB.objects.filter(protocolID__exact = protocol_id).exists():
                    station_obj = RequestForStationB.objects.filter(protocolID__exact = protocol_id).last()
                    return station_obj.get_user_file_obj()
            elif station == 'Station A':
                if protocol == '1':
                    if RequestForStationA_Prot1.objects.filter(protocolID__exact = protocol_id).exists():
                        station_obj = RequestForStationA_Prot1.objects.filter(protocolID__exact = protocol_id).last()
                        return station_obj.get_user_file_obj()
                elif protocol == '2':
                    if RequestForStationA_Prot2.objects.filter(protocolID__exact = protocol_id).exists():
                        station_obj = RequestForStationA_Prot2.objects.filter(protocolID__exact = protocol_id).last()
                        return station_obj.get_user_file_obj()
                else:
                    if RequestForStationA_Prot3.objects.filter(protocolID__exact = protocol_id).exists():
                        station_obj = RequestForStationA_Prot3.objects.filter(protocolID__exact = protocol_id).last()
                        return station_obj.get_user_file_obj()
    return None


def get_robot_station_type(robot_id):
    '''
    Function:
        The function get the station type which robot belongs to
    Inputs:
        robot_id     # robot id to find the station
    Return:
        file_mapping_obj. None if not match
    '''
    if RobotsInventory.objects.filter(robots__exact = robot_id).exists() :
        return RobotsInventory.objects.filter(robots__exact = robot_id).last().get_station_name()
    else:
        return None


def get_station_and_protocol(protocol_id):
    '''
    Function:
        The function get the station number and the prototocol used for the protocol id
    Inputs:
        protocol_id     # protocol id for getting the station and protocol
    Return:
        station_name, protocol_name .None if does not exist
    '''
    if FileIDUserRequestMapping.objects.filter(fileID__exact = protocol_id).exists():
        file_maping_obj = FileIDUserRequestMapping.objects.filter(fileID__exact = protocol_id).last()
        return (file_maping_obj.get_station(), file_maping_obj.get_station_protocol())
    return (None, None)

def store_and_find_changes_parameter_values(parameters, robot_action_obj):
    '''
    Function:
        store the parameters checking if the parameter value was changed from the
        data recorded when protocol file was recorded.
    Inputs:
        parameters      # in the POST request
        robot_action_obj    # object of the robot_action
    Functions:
        check_valid_date_format     # located at this file
    Return:
        True if all parameters remains unchanged. False at least one parameter was changed
    '''
    protocol_id = robot_action_obj.get_protocol_id()
    parameters_values_in_protocol_request = {}
    if ProtocolRequest.objects.filter(protocolID__exact = protocol_id).exists():
        protocol_request_obj = ProtocolRequest.objects.filter(protocolID__exact = protocol_id).last()
        if ProtocolParameterValues.objects.filter(protocolRequest = protocol_request_obj).exists():
            param_values = ProtocolParameterValues.objects.filter(protocolRequest = protocol_request_obj)

            for param_value in param_values:
                parameter, value = param_value.get_name_and_value()
                parameters_values_in_protocol_request[parameter] = value

    else:
        protocol_request_obj = None

    '''
    file_mapping_obj = get_file_mapping_obj_from_protocol_id (protocol_id)
    station , station_protocol = get_station_and_protocol(protocol_id)


    if station == 'Station C':
        if station_protocol == '1':
            if RequestForStationC_Prot1.objects.filter(protocolID__exact = protocol_id).exists():
                req_station_obj = RequestForStationC_Prot1.objects.filter(protocolID__exact = protocol_id).last()
                mapping_variables_dict = dict(MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_C_PROT_1)
        else:
            if RequestForStationC_Prot2.objects.filter(protocolID__exact = protocol_id).exists():
                req_station_obj = RequestForStationC_Prot2.objects.filter(protocolID__exact = protocol_id).last()
                mapping_variables_dict = dict(MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_C_PROT_2)
    elif station == 'Station B':
        if RequestForStationB.objects.filter(protocolID__exact = protocol_id).exists():
            req_station_obj = RequestForStationB.objects.filter(protocolID__exact = protocol_id).last()
            mapping_variables_dict = dict(MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_B)
    elif station == 'Station A':
        if station_protocol == '1':
            if RequestForStationA_Prot1.objects.filter(protocolID__exact = protocol_id).exists():
                req_station_obj = RequestForStationA_Prot1.objects.filter(protocolID__exact = protocol_id).last()
                mapping_variables_dict = dict(MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_A_PROT_1)
        elif station_protocol == '2':
            if RequestForStationA_Prot2.objects.filter(protocolID__exact = protocol_id).exists():
                req_station_obj = RequestForStationA_Prot2.objects.filter(protocolID__exact = protocol_id).last()
                mapping_variables_dict = dict(MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_A_PROT_2)
        else:
            if RequestForStationA_Prot3.objects.filter(protocolID__exact = protocol_id).exists():
                req_station_obj = RequestForStationA_Prot3.objects.filter(protocolID__exact = protocol_id).last()
                mapping_variables_dict = dict(MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_A_PROT_3)
    '''
    modified = False
    parameters_values_in_protocol_request
    for par in parameters.keys():
        request_data = {}
        request_data['robotActionPost'] = robot_action_obj
        request_data['protocolID'] = protocol_id
        request_data['parameterName'] = par
        request_data['parameterValue'] = parameters[par]
        request_data['ProtocolRequest'] = protocol_request_obj

        try:
            ### use the object attribute to get the value
            if str(parameters[par]) ==  str(parameters_values_in_protocol_request[par]):
                request_data['modified'] = False
            else :
                request_data['modified'] = True
                modified = True
        except:
            request_data['modified'] = True
            modified = True
        new_parameter = ParametersRobotAction.objects.create_parameter(request_data)

    return modified
