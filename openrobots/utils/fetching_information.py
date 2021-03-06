import time, re, json
from datetime import datetime
from datetime import timedelta
from openrobots.models import *
from openrobots.openrobots_config import *
from openrobots.utils.file_utilities import add_parameters_in_file

def get_action_robot_detail(action_id):
    '''
    Description:
        The function collect the parameter used in the robot action .
        Information is divided for modified and not modified parameters
    Functions:
        get_station_and_protocol   # located at this file
        get_station_from_template           # located at this file
    Return:
        detail_data
    '''
    detail_data = {}

    robot_action_obj = RobotsActionPost.objects.get(pk__exact = action_id)

    detail_data['main_data'] = [robot_action_obj.get_robot_action_data()]

    protocol_id = robot_action_obj.get_protocol_id()

    if ParametersRobotAction.objects.filter(robotActionPost = robot_action_obj).exists():
        parameters = ParametersRobotAction.objects.filter(robotActionPost = robot_action_obj).order_by('parameterName')
        detail_data['param_not_modified'] = []
        detail_data['param_modified'] = []
        for parameter in parameters:
            if parameter.get_modified_field():
                detail_data['param_modified'].append(parameter.get_parameter_name_and_value())
            else:
                detail_data['param_not_modified'].append(parameter.get_parameter_name_and_value())
        return detail_data
    return None


    '''
    #station, protocol = get_station_and_protocol(protocol_id)
    if station and protocol:
        requested_user_file_obj = get_requested_file_obj_from_station_protocol(station,protocol,protocol_id)
        parameters_dict = get_parameters_names_defined(station, protocol)
        detail_data['main_data'] = [robot_action_obj.get_robot_action_data()]

        if ParametersRobotAction.objects.filter(robotActionPost = robot_action_obj, protocolFileID__fileID__exact = protocol_id).exists():
            parameter_objs = ParametersRobotAction.objects.filter(robotActionPost = robot_action_obj, protocolFileID__fileID__exact = protocol_id)
            action_robot_parameters = {}
            for parameter_obj in parameter_objs:
                action_par_name, action_par_value = parameter_obj.get_parameter_name_and_value()
                action_robot_parameters[action_par_name] = action_par_value
        for par in parameters_dict.keys():
            try:
                ### use the object attribute to get the value

                if str(action_robot_parameters[par]) ==  str(getattr(requested_user_file_obj, parameters_dict[par])):
                    detail_data['param_not_modified'].append([par,action_robot_parameters[par]])

                else :
                    detail_data['param_modified'].append([par,action_robot_parameters[par], str(getattr(requested_user_file_obj, parameters_dict[par]))])
                    modified = True
            except:
                detail_data['param_not_found'].append([par, str(getattr(requested_user_file_obj, parameters_dict[par]))])
                modified = True

        return detail_data

    return False
    '''


# def  build_protocol_file_name(user, template):
    '''
    Description:
        The function build the protocol file name by joining the user, protocol_type, station and time
    Functions:
        get_protocol_type_from_template   # located at this file
        get_station_from_template           # located at this file
    Return:
        protocol_file_name
    '''
    '''
    name = [user]

    name.append(''.join(get_protocol_type_from_template(template).split()))
    name.append(''.join(get_station_from_template(template).split()))

    name.append(time.strftime("%Y%m%d-%H%M%S"))

    return '_'.join(name) + '.py'
    '''

def  build_protocol_request_file_name(user, template_id):
    '''
    Description:
        The function build the protocol file name by joining the user, protocol_type, station and time
    Functions:
        get_protocol_type_from_template_id   # located at this file
        get_station_from_template_id           # located at this file
    Return:
        protocol_file_name
    '''
    name = [user]

    name.append(''.join(get_protocol_type_from_template_id(template_id).split()))
    name.append(''.join(get_station_from_template_id(template_id).split()))

    name.append(time.strftime("%Y%m%d-%H%M%S"))

    return '_'.join(name) + '.py'

def build_request_codeID (user, protocol_type, station, protocol ) :
    '''
    Description:
        The function build the request codeID by joining the user, protocol_type, station and
        the number of times that this combination is used
    Input :
        user                # user objects
        protocol_type       # type of protocol
        station             # station used in the protocol

    Return:
        request codeID string
    '''
    num_times = 0
    if station == 'Station C':
        if RequestForStationC_Prot1.objects.filter(userRequestedBy = user, usedTemplateFile__typeOfProtocol__protocolTypeName__exact = protocol_type).exists():
            num_times = RequestForStationC_Prot1.objects.filter(userRequestedBy = user, usedTemplateFile__typeOfProtocol__protocolTypeName__exact = protocol_type).count()
    elif station == 'Station B':
        if RequestForStationB.objects.filter(userRequestedBy = user, usedTemplateFile__typeOfProtocol__protocolTypeName__exact = protocol_type).exists():
            num_times = RequestForStationB.objects.filter(userRequestedBy = user, usedTemplateFile__typeOfProtocol__protocolTypeName__exact = protocol_type).count()
    elif station == 'Station A':
        if protocol == '1':
            if RequestForStationA_Prot1.objects.filter(userRequestedBy = user, usedTemplateFile__typeOfProtocol__protocolTypeName__exact = protocol_type).exists():
                num_times = RequestForStationA_Prot1.objects.filter(userRequestedBy = user, usedTemplateFile__typeOfProtocol__protocolTypeName__exact = protocol_type).count()
        elif protocol == '2':
            if RequestForStationA_Prot2.objects.filter(userRequestedBy = user, usedTemplateFile__typeOfProtocol__protocolTypeName__exact = protocol_type).exists():
                num_times = RequestForStationA_Prot2.objects.filter(userRequestedBy = user, usedTemplateFile__typeOfProtocol__protocolTypeName__exact = protocol_type).count()
        else:
            if RequestForStationA_Prot3.objects.filter(userRequestedBy = user, usedTemplateFile__typeOfProtocol__protocolTypeName__exact = protocol_type).exists():
                num_times = RequestForStationA_Prot3.objects.filter(userRequestedBy = user, usedTemplateFile__typeOfProtocol__protocolTypeName__exact = protocol_type).count()

    num_times += 1
    return user.username + protocol_type + station + str(num_times)


def check_valid_date_format (date):
    '''
    Description:
        Function check if date has a valid format
    Return:
        True if valid
    '''
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except:
        return False

def check_empty_fields (row_data):
    '''
    Description:
        The function check if row_data contains empty values.
    Input:
        row_data:       # data to be checked

    Return:
        True if all values are empty
    '''
    line = list(set(row_data))
    if line == [''] :
        return True
    return False

# def get_parameters_names_defined(station, protocol):
    '''
    Description:
        The function will return the parameters used for the station and protocol
    Constans:
        MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_A_PROT_1
        PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_A_PROT_2
        PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_A_PROT_3
        PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_B
        PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_C_PROT_1
        PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_C_PROT_2
    Return:
        dictionary with parameter and values
    '''
    '''
    if station == 'Station A' and protocol == '1':
        return dict(MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_A_PROT_1)
    if station == 'Station A' and protocol == '2':
        return dict(MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_A_PROT_2)
    if station == 'Station A' and protocol == '3':
        return dict(MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_A_PROT_3)
    if station == 'Station B' and protocol == '1':
        return dict(MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_B)
    if station == 'Station C' and protocol == '1':
        return dict(MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_C_PROT_1)
    if station == 'Station C' and protocol == '2':
        return dict(MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_C_PROT_2)
    return False
    '''
def get_form_data_creation_new_robot():
    '''
    Description:
        The function will get the robot inventory information to display in the form
    Functions:
        get_stations_names      # located at this file
        get_defined_modules      # located at this file
    Return:
        form_data
    '''
    form_data = {}
    form_data['stations'] = get_stations_names ()
    form_data['modules'] = get_defined_modules()
    return form_data

# def get_form_data_creation_run_file():
    '''
    Description:
        The function will get the Labware information used in the form to create the files
    Functions:

    Return:
        form_data
    '''
    '''
    form_data = {}
    form_data['mag_plate_data'] = []
    form_data['waste_plate_data'] =[]
    form_data['reagent_labware_data'] = []
    form_data['mm_labware_data'] = []
    form_data['mm_tube_labware_data']  = []
    form_data['pcr_labware_data'] = []
    form_data['elution_station_c_data'] = []
    form_data['elution_station_b_data'] = []
    form_data['master_mix_type_data'] = []
    form_data['buffer_labware_data'] = []
    form_data['destination_labware_data'] = []
    form_data['dest_tube_labware_data'] = []
    form_data['beads_labware_data'] = []
    form_data['plate_labware_data'] = []
    form_data['lysate_labware_data'] = []
    form_data['language_data'] = []
    form_data['tips300_default_data'] = []
    form_data['tips300_data'] = []
    form_data['tips1000_default_data'] = []
    form_data['tips1000_data'] = []


    # values for station A form
    if MasterMixLabware.objects.all().exists():
        mm_labware_default_obj = MasterMixLabware.objects.filter(default = True).last()
        if mm_labware_default_obj:
            form_data['mm_labware_default_data'] = mm_labware_default_obj.get_mastermix_labware_type()
            mm_labwares = MasterMixLabware.objects.exclude(pk__exact = mm_labware_default_obj.pk)
        else:
            mm_labwares = MasterMixLabware.objects.all().order_by('MasterMixLabwareType')
        for mm_labware in mm_labwares :
            form_data['mm_labware_data'].append(mm_labware.get_mastermix_labware_type())
    if MasterMixTube.objects.all().exists():
        mm_tube_default_obj = MasterMixTube.objects.filter(default = True).last()
        if mm_tube_default_obj:
            form_data['mm_tube_labware_default_data'] = mm_tube_default_obj.get_mastermix_tube()
            mm_tube_labwares = MasterMixTube.objects.exclude(pk__exact = mm_tube_default_obj.pk)
        else:
            mm_tube_labwares = MasterMixTube.objects.all().order_by('MasterMixTube')
        for mm_tube_labware in mm_tube_labwares :
            form_data['mm_tube_labware_data'] .append(mm_tube_labware.get_mastermix_tube())
    if PCR_plateLabware.objects.all().exists():
        pcr_labware_default_obj = PCR_plateLabware.objects.filter(default = True).last()
        if pcr_labware_default_obj:
            form_data['pcr_labware_default_data'] = pcr_labware_default_obj.get_pcr_plate_labware_type()
            pcr_labwares = PCR_plateLabware.objects.exclude(pk__exact = pcr_labware_default_obj.pk)
        else:
            pcr_labwares = PCR_plateLabware.objects.all().order_by('PCR_plateLabwareType')
        for pcr_labware in pcr_labwares :
            form_data['pcr_labware_data'].append(pcr_labware.get_pcr_plate_labware_type())


    if ElutionStationC_Labware.objects.all().exists():
        elution_c_default_obj = ElutionStationC_Labware.objects.filter(default = True).last()
        if elution_c_default_obj:
            form_data['elution_station_c_default_data'] = elution_c_default_obj.get_elution_station_c()
            elution_c_types = ElutionStationC_Labware.objects.exclude(pk__exact = elution_c_default_obj.pk)
        else:
            elution_c_types = ElutionStationC_Labware.objects.all()
        for elution_c_type in elution_c_types:
            form_data['elution_station_c_data'].append(elution_c_type.get_elution_station_c())


    if MasterMixType.objects.all().exists():
        master_mix_default_obj = MasterMixType.objects.filter(default = True).last()
        if master_mix_default_obj:
            form_data['master_mix_type_default_data'] = master_mix_default_obj.get_master_mix_type()
            master_mix_types = MasterMixType.objects.exclude(pk__exact = master_mix_default_obj.pk)
        else:
            master_mix_types = MasterMixType.objects.all().order_by('MasterMixType')
        for master_mix_type in master_mix_types :
            form_data['master_mix_type_data'].append(master_mix_type.get_master_mix_type())

    # values for station B form
    if MagPlate_Labware.objects.all().exists():
        mag_default_obj = MagPlate_Labware.objects.filter(default = True).last()
        if mag_default_obj:
            form_data['mag_plate_default_data'] = mag_default_obj.get_mag_plate_name()
            mag_plates = MagPlate_Labware.objects.exclude(pk__exact = mag_default_obj.pk)
        else:
            mag_plates = MagPlate_Labware.objects.all()
        for mag_plate in mag_plates:
            form_data['mag_plate_data'].append(mag_plate.get_mag_plate_name())
    if Waste_Labware.objects.all().exists():
        waste_default_obj = Waste_Labware.objects.filter(default = True).last()
        if waste_default_obj:
            form_data['waste_plate_default_data'] =waste_default_obj.get_waste_labware_name()
            wastes_lab = Waste_Labware.objects.exclude(pk__exact = waste_default_obj.pk)
        else:
            wastes_lab = Waste_Labware.objects.all()
        for waste_lab in wastes_lab:
            form_data['waste_plate_data'].append(waste_lab.get_waste_labware_name())
    if Reagent_Labware.objects.all().exists():
        reagent_default_obj = Reagent_Labware.objects.filter(default = True).last()
        if reagent_default_obj:
            form_data['reagent_labware_default_data'] = reagent_default_obj.get_reagent_labware_name()
            reagents_lab = Reagent_Labware.objects.exclude(pk__exact = reagent_default_obj.pk)
        else:
            reagents_lab = Reagent_Labware.objects.all()
        for reagent_lab in reagents_lab:
            form_data['reagent_labware_data'].append(reagent_lab.get_reagent_labware_name())
    if ElutionStationB_Labware.objects.all().exists():
        elution_b_default_obj = ElutionStationB_Labware.objects.filter(default = True).last()
        if elution_b_default_obj:
            form_data['elution_station_b_default_data'] = elution_b_default_obj.get_elution_station_b()
            elution_b_types = ElutionStationB_Labware.objects.exclude(pk__exact = elution_b_default_obj.pk)
        else:
            elution_b_types = ElutionStationB_Labware.objects.all()
        for elution_b_type in elution_b_types:
            form_data['elution_station_b_data'].append(elution_b_type.get_elution_station_b())



    # values for station A form
    if Buffer_Labware.objects.all().exists():
        buffer_default_obj = Buffer_Labware.objects.filter(default = True).last()
        if buffer_default_obj:
            form_data['buffer_labware_default_data'] = buffer_default_obj.get_buffer_name()
            buffer_types = Buffer_Labware.objects.exclude(pk__exact = buffer_default_obj.pk)
        else:
            buffer_types = Buffer_Labware.objects.all()
        for buffer_type in buffer_types:
            form_data['buffer_labware_data'].append(buffer_type.get_buffer_name())
    if Destination_Labware.objects.all().exists():
        destination_default_obj = Destination_Labware.objects.filter(default = True).last()
        if destination_default_obj:
            form_data['destination_labware_default_data'] = destination_default_obj.get_destination_labware_name()
            destination_types = Destination_Labware.objects.exclude(pk__exact = destination_default_obj.pk)
        else:
            destination_types = Destination_Labware.objects.all()
        for destination_type in destination_types:
            form_data['destination_labware_data'].append(destination_type.get_destination_labware_name())
    if Destination_Tube_Labware.objects.all().exists():
        dest_tube_default_obj = Destination_Tube_Labware.objects.filter(default = True).last()
        if dest_tube_default_obj:
            form_data['dest_tube_labware_default_data'] = dest_tube_default_obj.get_destination_tube_name()
            destination_tubes = Destination_Tube_Labware.objects.exclude(pk__exact = dest_tube_default_obj.pk)
        else:
            destination_tubes = Destination_Tube_Labware.objects.all()
        for destination_tube in destination_tubes:
            form_data['dest_tube_labware_data'].append(destination_tube.get_destination_tube_name())
    if Beads_Labware.objects.all().exists():
        bead_default_obj = Beads_Labware.objects.filter(default = True).last()
        if bead_default_obj:
            form_data['beads_labware_default_data'] = bead_default_obj.get_beads_labware_name()
            bead_types = Beads_Labware.objects.exclude(pk__exact = bead_default_obj.pk)
        else:
            bead_types = Beads_Labware.objects.all()
        for bead_type in bead_types:
            form_data['beads_labware_data'].append(bead_type.get_beads_labware_name())
    if Plate_Labware.objects.all().exists():
        plate_default_obj = Plate_Labware.objects.filter(default = True).last()
        if plate_default_obj:
            form_data['plate_labware_default_data'] = plate_default_obj.get_plate_labware_name()
            plate_types = Plate_Labware.objects.exclude(pk__exact = plate_default_obj.pk)
        else:
            plate_types = Plate_Labware.objects.all()
        for plate_type in plate_types:
            form_data['plate_labware_data'].append(plate_type.get_plate_labware_name())
    if Lysate_Labware.objects.all().exists():
        lysate_default_obj = Lysate_Labware.objects.filter(default = True).last()
        if lysate_default_obj:
            form_data['lysate_labware_default_data'] = lysate_default_obj.get_lysate_labware_name()
            lysate_types = Lysate_Labware.objects.exclude(pk__exact = lysate_default_obj.pk)
        else:
            lysate_types = Lysate_Labware.objects.all()
        for lysate_type in lysate_types:
            form_data['lysate_labware_data'].append(lysate_type.get_lysate_labware_name())

    if Language.objects.all().exists():
        language_default_obj = Language.objects.filter(default = True).last()
        if language_default_obj:
            form_data['language_default_data'] = language_default_obj.get_language_code()
            language_types = Language.objects.exclude(pk__exact = language_default_obj.pk)
        else:
            language_types = Language.objects.all()
        for language_type in language_types:
            form_data['language_data'].append(language_type.get_language_code())
    if Tips300_Labware.objects.all().exists():
        tips300_default_obj = Tips300_Labware.objects.filter(default = True).last()
        if tips300_default_obj:
            form_data['tips300_default_data'] = tips300_default_obj.get_tips300_labware()
            tips300_types = Tips300_Labware.objects.exclude(pk__exact = tips300_default_obj.pk)
        else:
            tips300_types = Tips300_Labware.objects.all()
        for tips300_type in tips300_types :
            form_data['tips300_data'].append(tips300_type.get_tips300_labware())

    if Tips1000_Labware.objects.all().exists():
        tips1000_default_obj = Tips1000_Labware.objects.filter(default = True).last()
        if tips1000_default_obj:
            form_data['tips1000_default_data'] = tips1000_default_obj.get_tips1000_labware()
            tips1000_types = Tips1000_Labware.objects.exclude(pk__exact = tips1000_default_obj.pk)
        else:
            tips1000_types = Tips1000_Labware.objects.all()
        for tips1000_type in tips1000_types :
            form_data['tips1000_data'].append(tips1000_type.get_tips1000_labware())


    if ProtocolTemplateFiles.objects.filter(station__stationName__iexact = 'Station A').exists():
        form_data['station_a'] = {}
        protocol_types = ['Protocol 1', 'Protocol 2', 'Protocol 3']
        for i in range(len(protocol_types)) :
            if ProtocolTemplateFiles.objects.filter(station__stationName__iexact = 'Station A', protocolName__icontains = protocol_types[i]).exists():
                form_data['station_a'] [i+1]= ProtocolTemplateFiles.objects.filter(station__stationName__iexact = 'Station A', protocolName__icontains = protocol_types[i]).last().get_protocol_file_name()
    if ProtocolTemplateFiles.objects.filter(station__stationName__iexact = 'Station B').exists():
        form_data['station_b'] = ProtocolTemplateFiles.objects.filter(station__stationName__iexact = 'Station B').last().get_protocol_file_name()
    if ProtocolTemplateFiles.objects.filter(station__stationName__iexact = 'Station C').exists():
        form_data['station_c'] = {}
        protocol_types = ['Protocol 1', 'Protocol 2']
        for i in range(len(protocol_types)) :
            if ProtocolTemplateFiles.objects.filter(station__stationName__iexact = 'Station C', protocolName__icontains = protocol_types[i]).exists():
                form_data['station_c'][i+1] = ProtocolTemplateFiles.objects.filter(station__stationName__iexact = 'Station C', protocolName__icontains = protocol_types[i]).last().get_protocol_file_name()

    return form_data
    '''
def get_parameters_values_from_template(reference_template):
    '''
    Description:
        The function will get the parameters defined on the protocol template
    Return:
        parameter_values
    '''
    parameter_values = []
    parameters = ProtocolParameter.objects.filter(usedTemplateFile = reference_template)
    for parameter in parameters:
        parameter_type = parameter.get_parameter_type()
        param_data = ['']*len(PARAMETER_DEFINE_HEADING)
        data = parameter.get_parameter_info()
        param_data[0] = data[0]
        param_data[1] = data[1]
        param_data[2] = parameter_type
        if parameter_type != 'Option':
            param_data[5] = data[2]
            parameter_values.append(param_data)
        else:
            if ParameterOption.objects.filter(parameter = parameter).exists():
                param_options = ParameterOption.objects.filter(parameter = parameter)
                option_first_line = True
                for param_option in param_options:
                    if not option_first_line :
                        param_data = ['']*len(PARAMETER_DEFINE_HEADING)
                    else:
                        option_first_line = False
                    param_data[3] = param_option.get_option_value()
                    param_data[4] = param_option.get_option_description()
                    if param_data[3] == data[2]:
                        param_data[5] = 'X'
                    parameter_values.append(param_data)


    return parameter_values

def get_form_data_define_parameter(template_obj):
    '''
    Description:
        The function will get information to include in the parameter definition form
    Return:
        define_parameter
    '''
    define_parameter ={}
    define_parameter['type_available'] = PARAMETERS_TYPE
    define_parameter['heading'] = PARAMETER_DEFINE_HEADING
    if not template_obj :
        return define_parameter
    protocol = template_obj.get_protocol_number()
    version = template_obj.get_protocol_version()
    station = template_obj.get_station()
    protocol_type_obj = template_obj.get_protocol_type_obj()
    if ProtocolTemplateFiles.objects.filter(protocolTemplateBeUsed = True, station__stationName__exact = station,  typeOfProtocol = protocol_type_obj , protocolStationNumber__exact = protocol, protocolVersion__exact = version).exists():
        reference_template = ProtocolTemplateFiles.objects.filter(protocolTemplateBeUsed = True, station__stationName__exact = station, protocolStationNumber__exact = protocol, protocolVersion__exact = version).last()
        define_parameter['parameter_values'] = get_parameters_values_from_template(reference_template)

    return  define_parameter


def get_form_data_robots_usage():
    '''
    Description:
        The function will get information to include in the robot usage form
    Return:
        form_data
    '''
    form_data = {}
    form_data['stations'] = []
    if Stations.objects.all().exists():
        stations = Stations.objects.all()
        for station in stations:
            form_data['stations'].append(station.get_station_name())
    if RobotsActionPost.objects.all().exists():
        robots_list = []
        protocols_action_list = []
        robot_objs = RobotsActionPost.objects.all()
        for robot_obj in robot_objs:
            robots_list.append(robot_obj.get_robot_name())
            protocols_action_list.append(robot_obj.get_executed_action())
        form_data['robots'] = list(set(robots_list))
        form_data['protocols_action'] = list(set(protocols_action_list))

    return form_data

def get_input_define_parameter(form_data):
    '''
    Description:
        The function get the parameter defined by user for the protocol
    Constans:
        PARAMETER_DEFINE_IN_DDBB
    Functions:
        check_empty_fields      # located at this file
    Return:
        parameter_data and valid_form
    '''
    parameter_data = []
    parameter_json_data = json.loads(form_data['parameter_data'])
    option_parameter = False
    valid_form = True
    for row_index in range(len(parameter_json_data)) :
        if check_empty_fields(parameter_json_data[row_index]):
            continue
        # remove empty space at start and end of the item list
        for j in range(len(parameter_json_data[row_index])):
            parameter_json_data[row_index][j] = parameter_json_data[row_index][j].strip()
        if (parameter_json_data[row_index][0] == '' or parameter_json_data[row_index][1] == '') and not option_parameter :
            valid_form = False
            continue
        elif (parameter_json_data[row_index][0] == '' or parameter_json_data[row_index][1] == '') and option_parameter:
            row_data[PARAMETER_DEFINE_IN_DDBB[3]].append(parameter_json_data[row_index][3])
            row_data[PARAMETER_DEFINE_IN_DDBB[4]].append(parameter_json_data[row_index][4])
            if parameter_json_data[row_index][5].upper() == 'X' :
                row_data[PARAMETER_DEFINE_IN_DDBB[5]] = parameter_json_data[row_index][3]
            continue
        if option_parameter:
            parameter_data.append(row_data)
            option_parameter = False
        row_data = {}
        for i in range(len(PARAMETER_DEFINE_IN_DDBB)):
            row_data[PARAMETER_DEFINE_IN_DDBB[i]] = parameter_json_data[row_index][i]
        if parameter_json_data[row_index][2] == 'Option':
            row_data[PARAMETER_DEFINE_IN_DDBB[3]] = [parameter_json_data[row_index][3]]
            row_data[PARAMETER_DEFINE_IN_DDBB[4]] = [parameter_json_data[row_index][4]]
            if parameter_json_data[row_index][5].upper() == 'X' :
                row_data[PARAMETER_DEFINE_IN_DDBB[5]] = parameter_json_data[row_index][3]
            option_parameter = True
            continue
        parameter_data.append(row_data)

    return parameter_data, valid_form


def get_list_labware_inventory():
    '''
    Description:
        The function will get the labware availables and fetch for each inventory data
    Return:
        labware_data
    '''
    labware_data = []
    if InventoryLabware.objects.all().exists():
        elutions = InventoryLabware.objects.all().order_by('brand')
        for elution in elutions:
            labware_data.append(elution.get_minimun_elution_lab_data())
    return labware_data

def get_list_module_inventory():
    '''
    Description:
        The function will get the module availables and fetch for each inventory data
    Return:
        labware_data
    '''
    module_data = []
    if ModuleType.objects.all().exists():
        modules = ModuleType.objects.all().order_by('vendor')
        for module in modules:
            module_data.append(module.get_minimum_module_data())
    return module_data

def get_list_robot_inventory():
    '''
    Description:
        The function will get the robot availables and fetch for each inventory data
    Return:
        robot_data
    '''
    robot_data = []
    if RobotsInventory.objects.all().exists():
        robots_defined = RobotsInventory.objects.all().order_by('robots')
        for robot in robots_defined:
            robot_data.append(robot.get_minimum_robot_data())

    return robot_data

def get_defined_modules () :
    '''
    Description:
        The function get the defined module
    Return:

    '''
    module_data = []
    if ModulesInLab.objects.all().exists():
        modules = ModulesInLab.objects.all().order_by('moduleType')
        for module in modules:
            module_data.append([module.get_module_id(), module.get_module_type_and_ID()])

    return module_data

def get_elution_hw_types():
    '''
    Description:
        The function get the elution HW types defined
    Return:
        elution_hw_types
    '''
    elution_hw_types = []
    if ElutionHardware.objects.all().exists():
        elutions = ElutionHardware.objects.all().order_by('hardwareType')
        for elution in elutions:
            elution_hw_types.append(elution.get_hardware_type())
    return elution_hw_types


def get_labware_inventory_data(labware_id):
    '''
    Description:
        The function will fetch the labware inventory data
    Return:
        labware_data
    '''
    labware_data = {}
    if InventoryLabware.objects.filter(pk__exact = labware_id).exists():
        labware_obj = InventoryLabware.objects.get(pk__exact = labware_id)
        labware_data['main'] = labware_obj.get_basic_labware_data()
        labware_data['labware_name'] = labware_obj.get_elution_labware_type()
        labware_data['plate'] = labware_obj.get_plate_data()
        labware_data['well'] = labware_obj.get_well_data()
        labware_data['files'] = labware_obj.get_files()
        labware_data['image'] = labware_obj.get_image()


    return labware_data

def get_module_inventory_data(module_id):
    '''
    Description:
        The function will fetch the module inventory data
    Return:
        module_data
    '''
    module_data = {}
    if ModuleType.objects.filter(pk__exact = module_id).exists():
        module_obj = ModuleType.objects.get(pk__exact = module_id)
        module_data['main'] = module_obj.get_main_module_data()
        module_data['documents'] = module_obj.get_documents()
        module_data['image'] = module_obj.get_image()

    return module_data

def get_module_obj_from_id(module_id):
    if ModulesInLab.objects.filter(pk__exact = module_id):
        return ModulesInLab.objects.get(pk__exact = module_id)
    return None


# def get_requested_file_obj_from_station_protocol(station,protocol, protocol_file_id):
    '''
    Description:
        The function get the query object for the station. protocol, protocol_file_id
    Return:
        requested_file_obj
    '''
    '''
    if station == 'Station A' and protocol == '1':
        if RequestForStationA_Prot1.objects.filter(protocolID__exact = protocol_file_id).exists():
            return RequestForStationA_Prot1.objects.filter(protocolID__exact = protocol_file_id).last()
    if station == 'Station A' and protocol == '2':
        if RequestForStationA_Prot2.objects.filter(protocolID__exact = protocol_file_id).exists():
            return RequestForStationA_Prot2.objects.filter(protocolID__exact = protocol_file_id).last()
    if station == 'Station A' and protocol == '3':
        if RequestForStationA_Prot3.objects.filter(protocolID__exact = protocol_file_id).exists():
            return RequestForStationA_Prot3.objects.filter(protocolID__exact = protocol_file_id).last()
    if station == 'Station B' and protocol == '1':
        if RequestForStationB.objects.filter(protocolID__exact = protocol_file_id).exists():
            return RequestForStationB.objects.filter(protocolID__exact = protocol_file_id).last()
    if station == 'Station C' and protocol == '1':
        if RequestForStationC_Prot1.objects.filter(protocolID__exact = protocol_file_id).exists():
            return RequestForStationC_Prot1.objects.filter(protocolID__exact = protocol_file_id).last()
    if station == 'Station C' and protocol == '2':
        if RequestForStationC_Prot2.objects.filter(protocolID__exact = protocol_file_id).exists():
            return RequestForStationC_Prot2.objects.filter(protocolID__exact = protocol_file_id).last()

    return False
    '''
def get_robot_inventory_data(robot_id):
    '''
    Description:
        The function will fetch the robot inventory data
    Return:
        robot_data
    '''
    robot_data = {}
    if RobotsInventory.objects.filter(pk__exact = robot_id).exists():
        robot_obj = RobotsInventory.objects.get(pk__exact = robot_id)
        robot_data['main'] = robot_obj.get_basic_robot_data()
        robot_data['robot_name'] = robot_obj.get_robot_name()
        robot_data['network'] = robot_obj.get_network_data()
        robot_data['pipette'] = robot_obj.get_pipette_data()
        robot_data['plugs'] = robot_obj.get_plugs_data()

        modules = robot_obj.modules.all()
        robot_data['modules'] = []
        for module in modules :
            robot_data['modules'].append([module.get_module_type(), module.get_moduleID()])

    return robot_data

def get_robots_action_from_user_form(form_data ):
    '''
    Description:
        The function will the objects for the robot action that match user data
        in the form. If start date is empty the query only check the
        end_date. On the contrary if end_date is not given the match will be done
        until today, If no dates are given the matches are limited to today
    Inputs:
        form_data      # data from user form
    Functions:
        get_today_and_tomorrows_day     # located at this file
    Return:
        robots_actions_objs or None
    '''
    if RobotsActionPost.objects.all().exists():
        start_date = form_data['startdate']
        end_date = form_data['enddate']

        if start_date == '' and end_date == '':
            #if empty values set the date to today and tomorrow
            start_date, end_date = get_today_and_tomorrows_day()

        # only end_date is defined
        if start_date == '' and end_date != '':
            if RobotsActionPost.objects.filter(generatedat__lte = end_date).exists():
                robots_actions_objs = RobotsActionPost.objects.filter(generatedat__lte = end_date).order_by('generatedat')
            else:
                return None
        # only start date is difined
        if end_date == '' and start_date != '':
            if RobotsActionPost.objects.filter(generatedat__gte = start_date).exists():
                robots_actions_objs =  RobotsActionPost.objects.filter(generatedat__gte = start_date).order_by('generatedat')
            else:
                return None
        if end_date != '' and start_date != '':
            if  RobotsActionPost.objects.filter(generatedat__range=(start_date, end_date )).exists():
                robots_actions_objs =  RobotsActionPost.objects.filter(generatedat__range=(start_date, end_date )).order_by('generatedat')
            else:
                return None
        if form_data['robots'] != '':
            if robots_actions_objs.filter(RobotID__exact = form_data['robots']).exists():
                robots_actions_objs = robots_actions_objs.filter(RobotID__exact = form_data['robots'])
            else:
                return None
        if form_data['stations'] != '':
            if robots_actions_objs.filter(stationType__exact = form_data['stations']).exists():
                robots_actions_objs = robots_actions_objs.filter(stationType__exact = form_data['stations'])
            else:
                return None
        if form_data['protocolsAction'] != '':
            if robots_actions_objs.filter(executedAction__exact = form_data['protocolsAction']).exists():
                robots_actions_objs = robots_actions_objs.filter(executedAction__exact = form_data['protocolsAction'])
            else:
                return None
        return  robots_actions_objs
    else:
        return None

def get_protocol_and_station_defined ():
    '''
    Description:
        The function will fetch the protocol numbers for each station defined
    Return:
        station_protocol_number
    '''
    station_protocol_number =  []
    if ProtocolosInStation.objects.all().exists():
        
        p_nunbers = ProtocolosInStation.objects.all().order_by('station__stationName')
        for p_nunber in p_nunbers :
            station_protocol_number.append(STRING_TO_SEPARATE_STATION_AND_PROTOCOL_NUMBER.join(p_nunber.get_station_and_protocol()))
    return station_protocol_number

def get_protocol_types():
    '''
    Description:
        The function will fetch the protocol types defined
    Return:
        protocol_types
    '''
    protocol_types =  []
    if ProtocolsType.objects.all().exists():
        p_types = ProtocolsType.objects.all().order_by('protocolTypeName')
        for p_type in p_types :
            protocol_types.append(p_type.get_name())
    return protocol_types


def get_protocol_template_information(p_template_id):
    '''
    Description:
        The function will fetch the information for protocol template
    Return:
        protocol_data
    '''
    protocol_data = {}
    if ProtocolTemplateFiles.objects.filter(pk__exact = p_template_id).exists():
        p_template = ProtocolTemplateFiles.objects.get(pk__exact = p_template_id)
        protocol_data['basic_data'] = [p_template.get_main_data()]
        protocol_data['metadata'] = p_template.get_metadata()

        if ProtocolParameter.objects.filter(usedTemplateFile =  p_template).exists():
            protocol_data['parameters'] = []
            protocol_parameter_objs = ProtocolParameter.objects.filter(usedTemplateFile =  p_template)
        for protocol_parameter_obj in protocol_parameter_objs:
            protocol_data['parameters'].append(protocol_parameter_obj.get_parameter_info())
    return protocol_data

def get_protocol_type_from_template_id(template_id):
    '''
    Description:
        The function will fetch the protocol type from protocol template id
    Return:
        protocol_type
    '''
    if ProtocolTemplateFiles.objects.filter(pk__exact = template_id).exists() :
        return ProtocolTemplateFiles.objects.get(pk__exact = template_id).get_protocol_type()
    return 'None'

def get_protocol_type_from_template(template):
    '''
    Description:
        The function will fetch the protocol type from protocol template
    Return:
        protocol_type
    '''
    if ProtocolTemplateFiles.objects.filter(protocolTemplateFileName__exact = template).exists() :
        return ProtocolTemplateFiles.objects.get(protocolTemplateFileName__exact = template).get_protocol_type()
    return 'None'

def get_robots_information_utilization(robots_action_obj):
    '''
    Description:
        The function will look for robot jobs in the period of time between start_date
        and end_date.
        graphic_about utilization and jobs executed per robots are returned
    Return:
        robot_jobs_data
    '''
    robot_jobs_data = {}
    robot_jobs_data['actions'] = {}
    robot_jobs_data['robot_usage'] = {}
    robot_jobs_data['grafic'] = []
    protocols_used = []
    #robot_jobs_data[station_type]['robot_usage'] = 0
    #robot_jobs_data[station_type][robot_name]['robot_actions'] =[]
    for action_obj in robots_action_obj:
        station_type = action_obj.get_station_type().replace(' ','_')
        robot_name = action_obj.get_robot_name()
        if not station_type in robot_jobs_data['actions'] :
            robot_jobs_data['actions'][station_type] = {}

        if not robot_name in robot_jobs_data['actions'][station_type] :
            robot_jobs_data['actions'][station_type][robot_name] = []
        if not robot_name in robot_jobs_data['robot_usage']:
            robot_jobs_data['robot_usage'][robot_name] = 0

        robot_jobs_data['robot_usage'][robot_name] +=1
        robot_jobs_data['actions'][station_type][robot_name].append(action_obj.get_robot_action_data())
        protocols_used.append(action_obj.get_protocol_id())

    for key, val in robot_jobs_data['robot_usage'].items():
        temp_dict = {}
        temp_dict['name'] = key
        temp_dict['count'] = val
        robot_jobs_data['grafic'].append(temp_dict)
    # collect data for summary
    summary = {}
    summary['n_actions'] = sum(list(robot_jobs_data['robot_usage'].values()))
    summary['n_robots'] = len(robot_jobs_data['robot_usage'])
    summary['n_exec_prot'] = len(protocols_used)
    summary['n_dif_exec_prot'] = len(set(protocols_used))

    robot_jobs_data['summary'] = summary

    return robot_jobs_data

def get_station_from_template_id(template_id):
    '''
    Description:
        The function will fetch the station name from protocol template
    Return:
        station name
    '''
    if ProtocolTemplateFiles.objects.filter(pk__exact = template_id).exists() :
        protocol_template_obj = ProtocolTemplateFiles.objects.get(pk__exact = template_id)
        protocol_name = protocol_template_obj.get_protocol_name()
        try:
            prot_fields = re.search(r'.*Station [A|B|C] Protocol (\d+) (\w+) .*',protocol_name).groups()
            prot = '_'.join(prot_fields)
        except:
            prot = '1_Unkonwn'

        return protocol_template_obj.get_station() + '_Prot' + prot
    return 'None'


def get_station_from_template(template):
    '''
    Description:
        The function will fetch the station name from protocol template
    Return:
        station name
    '''
    if ProtocolTemplateFiles.objects.filter(protocolTemplateFileName__exact = template).exists() :
        protocol_template_obj = ProtocolTemplateFiles.objects.get(protocolTemplateFileName__exact = template)
        protocol_name = protocol_template_obj.get_protocol_name()
        try:
            prot_fields = re.search(r'.*Station [A|B|C] Protocol (\d+) (\w+) .*',protocol_name).groups()
            prot = '_'.join(prot_fields)
        except:
            prot = '1_Unkonwn'

        return protocol_template_obj.get_station() + '_Prot' + prot
    return 'None'

def get_stations_names ():
    '''
    Description:
        The function will fetch the stations defined
    Return:
        station_names
    '''
    station_names =  []
    if Stations.objects.all().exists():
        s_names = Stations.objects.all().order_by('stationName')
        for s_name in s_names :
            station_names.append(s_name.get_station_name())
    return station_names

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

def get_stored_protocols_files():
    '''
    Description:
        The function get the main information for the protocols templates defined
    Return:
        protocol_file_data
    '''
    protocol_file_data = {}

    if ProtocolTemplateFiles.objects.all().exists():
        p_templates = ProtocolTemplateFiles.objects.all().order_by('station').order_by('protocolStationNumber')
        for p_template in p_templates :
            station_name = p_template.get_station()
            prot_ver_number = p_template.get_protocol_number()
            if station_name not in protocol_file_data :
                protocol_file_data[station_name] = {}
            if not prot_ver_number in protocol_file_data[station_name]:
                protocol_file_data[station_name][prot_ver_number] = []
            protocol_file_data[station_name][prot_ver_number].append(p_template.get_main_data())
    return protocol_file_data


# def extract_form_data_station (request) :
    '''
    Description:
        The function extract the user form data and define a dictionnary with the values
    Constants:
        PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_C_PROT_1
        PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_C_PROT_2
        PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_B
        PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_A_PROT_1
        PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_A_PROT_2
        PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_A_PROT_3
    Return:
        valid_metadata
    '''
    '''
    data_for_file = {}
    data_for_file2 = {}
    data_for_database = {}
    if request.POST['station'] == 'Station C' and request.POST['protocol'] == '1':
        for item in PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_C_PROT_1:
            data_for_file[item] = request.POST[item]
        for item in MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_C_PROT_1 :
            data_for_database[item[1]] = request.POST[item[0]]
        data_for_database['station'] = 'Station C'
    elif request.POST['station'] == 'Station C' and request.POST['protocol'] == '2':
        for item in PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_C_PROT_2:
            data_for_file[item] = request.POST[item]
        #[(data_for_file2[item] = request.POST[item]) for item in PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_C ]
        for item in MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_C_PROT_2 :
            data_for_database[item[1]] = request.POST[item[0]]
        data_for_database['station'] = 'Station C'
    elif request.POST['station'] == 'Station B':
        for item in PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_B:
            data_for_file[item] = request.POST[item]
        #[(data_for_file2[item] = request.POST[item]) for item in PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_C ]
        for item in MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_B :
            data_for_database[item[1]] = request.POST[item[0]]

    elif  request.POST['station'] == 'Station A' and request.POST['protocol'] == '1' :
        for item in PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_A_PROT_1:
            data_for_file[item] = request.POST[item]
        for item in MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_A_PROT_1 :
            data_for_database[item[1]] = request.POST[item[0]]
    elif  request.POST['station'] == 'Station A' and request.POST['protocol'] == '2' :
        for item in PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_A_PROT_2:
            data_for_file[item] = request.POST[item]
        for item in MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_A_PROT_2 :
            data_for_database[item[1]] = request.POST[item[0]]
    elif  request.POST['station'] == 'Station A' and request.POST['protocol'] == '3' :
        for item in PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_A_PROT_3:
            data_for_file[item] = request.POST[item]
        for item in MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_A_PROT_3 :
            data_for_database[item[1]] = request.POST[item[0]]

    # Add common data to store on database
    data_for_database['usedTemplateFile'] = request.POST['template']
    data_for_database['userNotes'] = request.POST['usernotes']
    data_for_database['userRequestedBy'] = request.user

    return data_for_file , data_for_database
    '''
def extract_define_robot_form_data (request) :
    '''
    Description:
        The function extract the user form data and define a dictionnary with the values
    Return:
        robot_data
    '''
    form_field_list = ['configuration','location' ,'robots', 'serialNumber', 'IP_address', 'hostName',
            'computer_mac', 'rightPipette', 'leftPipette', 'rightPipetteID', 'leftPipetteID', 'neededPlugs', 'observations']
    robot_data = {}
    for item in form_field_list :
        robot_data[item] = request.POST[item]
    robot_data['modules'] = request.POST.getlist('modules')
    return robot_data


def get_list_of_requests():
    '''
    Description:
        The function get the list of the protocol requested files.
        They are split by station
    Return:
        request_list
    '''
    request_list = {}
    '''
    # get request for Station C protocols
    if RequestForStationC_Prot1.objects.all().exists():
        request_list['station_c'] = []
        c_requests = RequestForStationC_Prot1.objects.all().order_by('userRequestedBy').order_by('generatedat')
        for request in c_requests:
            request_list['station_c'].append(request.get_request_info())
    if RequestForStationB.objects.all().exists():
        request_list['station_b'] = []
        b_requests = RequestForStationB.objects.all().order_by('userRequestedBy').order_by('generatedat')
        for request in b_requests:
            request_list['station_b'].append(request.get_request_info())
    if RequestForStationA_Prot1.objects.all().exists():
        request_list['station_a_prot1'] = []
        a_prot1_requests = RequestForStationA_Prot1.objects.all().order_by('userRequestedBy').order_by('generatedat')
        for request in a_prot1_requests:
            request_list['station_a_prot1'].append(request.get_request_info())
    if RequestForStationA_Prot2.objects.all().exists():
        request_list['station_a_prot2'] = []
        a_prot1_requests = RequestForStationA_Prot2.objects.all().order_by('userRequestedBy').order_by('generatedat')
        for request in a_prot1_requests:
            request_list['station_a_prot2'].append(request.get_request_info())
    if RequestForStationA_Prot3.objects.all().exists():
        request_list['station_a_prot3'] = []
        a_prot1_requests = RequestForStationA_Prot3.objects.all().order_by('userRequestedBy').order_by('generatedat')
        for request in a_prot1_requests:
            request_list['station_a_prot3'].append(request.get_request_info())


    '''

    if ProtocolRequest.objects.all().exists():
        station_objs = Stations.objects.all().order_by('stationName')
        for station_obj in station_objs:
            if ProtocolRequest.objects.filter(protocolTemplate__station = station_obj).exists():
                station_requests = ProtocolRequest.objects.filter(protocolTemplate__station = station_obj).order_by('requestedCodeID')
                station_name = station_obj.get_station_name().lower().replace(' ','_')
                request_list[station_name] = []
                for request in station_requests:
                    request_list[station_name].append(request.get_request_info())

    return request_list

def get_pending_protocol_parameters():
    '''
    Description:
        The function get the protocol templates names and ids of the protocol templates
        which have not defined yet the parameters
    Return:
        pending_protocols
    '''
    pending_protocols = []
    if ProtocolTemplateFiles.objects.filter(parametersDefined__exact = False).exists():
        protocols = ProtocolTemplateFiles.objects.filter(parametersDefined__exact = False)
        for protocol in protocols:
            pending_protocols.append(protocol.get_main_data())
    return pending_protocols


def get_protocol_template_obj_from_id(protocol_template_id):
    '''
    Description:
        The function get the instance object from the protocol template id
    Return:
        protocol_template_obj
    '''
    if ProtocolTemplateFiles.objects.filter(pk__exact = protocol_template_id).exists():
        return ProtocolTemplateFiles.objects.get(pk__exact = protocol_template_id)
    return False


def get_recorded_protocol_template(protocol_template_id) :
    '''
    Description:
        The function get protocol template name and the file
    Return:
        created_new_file
    '''
    created_new_file = {}
    protocol_obj = get_protocol_template_obj_from_id(protocol_template_id)
    created_new_file['protocol_name'] = protocol_obj.get_protocol_name()
    created_new_file['file_name'] = protocol_obj.get_protocol_file()
    return created_new_file

def increase_protocol_file_id ():
    '''
    Description:
        The function look for the latest file id value and increment in one unit.
        When reaching 9999 it will step up the letter
    Return:
        new_file_id
    '''
    # get the latest value stored in database
    if FileIDUserRequestMapping.objects.all().exists():
        last_index = FileIDUserRequestMapping.objects.last().get_file_id()
        index_number_str, index_letter = last_index.split('-')
        # increase the index number
        index_number = int(index_number_str) +1
        if index_number > 9999:
            index_number = 0
            # step up the letter
            split_index_letter = list(index_letter)
            if split_index_letter[1] == 'Z':
                last_letter = chr(ord(split_index_letter[0])+1)
                split_index_letter[0] = last_letter
                split_index_letter[1] = 'A'
                index_letter = ''.join(split_index_letter)
            else:
                first_letter=chr(ord(split_index_letter[1])+1)
                split_index_letter[1] = first_letter
                index_letter = ''.join(split_index_letter)

        index_number_str = str(index_number)
        index_number_str = index_number_str.zfill(4)
        return str(index_number_str + '-'+ index_letter)
    else:
        return '0000-AA'

def set_protocol_parameters_defined(protocol_template_id):
    '''
    Description:
        The function update the protocol template with parameter defined and set to be used
        If an older version of the protocol template it is set to not used
    Functions:
        get_protocol_template_obj_from_id   # located at this file
    Return:
        None
    '''

    protocol_template_obj = get_protocol_template_obj_from_id(protocol_template_id)
    station = protocol_template_obj.get_station()
    type_of_protocol = protocol_template_obj.get_protocol_type()
    protocol_number = protocol_template_obj.get_protocol_number()

    if ProtocolTemplateFiles.objects.filter(protocolTemplateBeUsed = True, station__stationName__exact = station, typeOfProtocol__protocolTypeName__exact = type_of_protocol, protocolStationNumber__protocolNumber__exact = protocol_number).exists():
        old_protocol_template = ProtocolTemplateFiles.objects.filter(protocolTemplateBeUsed = True, station__stationName__exact = station, typeOfProtocol__protocolTypeName__exact = type_of_protocol, protocolStationNumber__protocolNumber__exact = protocol_number).last()
        old_protocol_template.set_template_do_not_use()

    protocol_template_obj.set_parameters_defined()
    protocol_template_obj.set_template_to_be_used()
    return

def store_define_parameter(define_parameter_data, template_file_id):
    '''
    Description:
        The function store protocol parameters in database
    Return:
        None
    '''
    for parameter in define_parameter_data:
        new_parameter = ProtocolParameter.objects.create_parameter(parameter, template_file_id)

        if parameter['parameterType'] == 'Option':
            default_value = new_parameter.get_default_value()
            for i in range(len(parameter['optionValue'])):
                option_data = {}
                option_data['parameter'] = new_parameter
                option_data['optionValue'] = parameter['optionValue'][i]
                option_data['optionDescription'] = parameter['optionDescription'][i]
                if default_value == parameter['optionValue'][i]:
                    option_data['default'] = 'X'
                else:
                    option_data['default'] = None
                new_parameter_option = ParameterOption.objects.create_parameter_option(option_data)

    return

def store_file_id (protocol_file_id, station, protocol):
    '''
    Description:
        The function store in database to link the file_id with the station and protocol
    Return:
        new_file_id
    '''
    data = {}
    data['fileID'] = protocol_file_id
    data['station'] = station
    data['protocol'] = protocol
    new_file_id = FileIDUserRequestMapping.objects.create_file_id_user(data)
    return new_file_id

def get_today_and_tomorrows_day():
    '''
    Description:
        Teh function get the day of today and tomorrow
    Return:
        today_day , tomorrow_day
    '''
    today = datetime.now()
    today_day = datetime.now().strftime('%Y-%m-%d')
    tomorrow_day = (today + timedelta(days=1)).strftime('%Y-%m-%d')

    return (today_day, tomorrow_day)

def robot_action_exists(action_id):
    '''
    Description:
        The function check if the action id exists
    Input:
        action_id       # Id of the action to check
    Return:
        True if exists False else
    '''
    if RobotsActionPost.objects.filter(pk__exact = action_id).exists():
        return True
    return False

def validate_metadata_for_protocol_template(metadata):
    '''
    Description:
        The function get only the metadata values defiened in METADATA_FIELDS_FOR_PROTOCOL_TEMPLATE
    Constants:
        METADATA_FIELDS_FOR_PROTOCOL_TEMPLATE
    Return:
        valid_metadata
    '''
    valid_metadata = {}
    # Set empty values if metadata tag is not found
    for item in METADATA_FIELDS_FOR_PROTOCOL_TEMPLATE:
        if item in metadata :
            valid_metadata[item] = metadata[item]
        else:
            valid_metadata[item] = ''
    return valid_metadata

def get_protocol_parameters(protocol, parameter_type):
    '''
    Description:
        The function get the parameter filter by type of parameters, used in the protocol.
    Input:
        protocol    # protocol object
        parameter_type      # type to filter the parameters used in the protocol
    Constants:

    Return:
        parameter_data
    '''
    parameter_data = []

    if ProtocolParameter.objects.filter(usedTemplateFile = protocol, parameterType__exact = parameter_type).exists():
        parameters = ProtocolParameter.objects.filter(usedTemplateFile = protocol, parameterType__exact = parameter_type).order_by('parameterName')
        for parameter in parameters:
            data = parameter.get_parameter_info()
            if parameter_type == 'Option':
                if ParameterOption.objects.filter(parameter = parameter).exists():
                    param_options = ParameterOption.objects.filter(parameter = parameter)
                    option_values =[]
                    default_value = parameter.get_default_value()
                    for param_option in param_options:
                        value = param_option.get_option_value()
                        if value != default_value:
                            option_values.append(value)

                    if len(option_values) == 0 :
                        option_values = ['']
                    data.append(option_values)
                else:
                    data.append([''])
            parameter_data.append(data)


    return parameter_data

def get_protocol_data_for_form (protocol):
    '''
    Description:
        The function get the input fields to display in the form
    Input:
        protocol        # protocol instance
    Constants:
        PARAMETERS_TYPE
    Return:
        data_form_protocol
    '''
    data_form_protocol ={}
    data_form_protocol['name_in_form'] = protocol.get_name_in_form()
    for parameter_type in PARAMETERS_TYPE :
        data_form_protocol[parameter_type] = get_protocol_parameters(protocol, parameter_type)
    data_form_protocol['template_id'] = protocol.get_protocol_template_id()
    return data_form_protocol

def get_defined_parameters_protocol_template (template_id):
    '''
    Description:
        The function get the parameter names defined in the protocol template
    Input:
        template_id     # protocol template id for the request
    Functions:
        get_protocol_template_obj_from_id   # Located at ths file
    Return:
        parameter_names
    '''
    parameter_names = []
    protocol_template_obj = get_protocol_template_obj_from_id(template_id)
    if ProtocolParameter.objects.filter(usedTemplateFile = protocol_template_obj).exists():
        parameters = ProtocolParameter.objects.filter(usedTemplateFile = protocol_template_obj).order_by('parameterName')
        for parameter in parameters:
            parameter_names.append(parameter.get_parameter_name())
    return parameter_names

def get_form_data_station_A():
    '''
    Description:
        The function get the available protocols and parameters for station A
    Constants:
        METADATA_FIELDS_FOR_PROTOCOL_TEMPLATE
    Return:
        data_form_station_a
    '''
    data_form_station_a = []
    if ProtocolTemplateFiles.objects.filter(station__stationName__exact = 'Station A', protocolTemplateBeUsed__exact = True).exists():
        protocols = ProtocolTemplateFiles.objects.filter(station__stationName__exact = 'Station A', protocolTemplateBeUsed__exact = True).order_by('protocolStationNumber')
        for protocol in protocols:
            data_form_station_a.append(get_protocol_data_for_form(protocol))

    return data_form_station_a

def get_form_data_station_B():
    '''
    Description:
        The function get the available protocols and parameters for station B
    Constants:
        METADATA_FIELDS_FOR_PROTOCOL_TEMPLATE
    Return:
        data_form_station_b
    '''
    data_form_station_b = []
    if ProtocolTemplateFiles.objects.filter(station__stationName__exact = 'Station B', protocolTemplateBeUsed__exact = True).exists():
        protocols = ProtocolTemplateFiles.objects.filter(station__stationName__exact = 'Station B', protocolTemplateBeUsed__exact = True).order_by('protocolStationNumber')
        for protocol in protocols:
            data_form_station_b.append(get_protocol_data_for_form(protocol))

    return data_form_station_b


def get_form_data_station_C():
    '''
    Description:
        The function get the available protocols and parameters for station C
    Constants:
        METADATA_FIELDS_FOR_PROTOCOL_TEMPLATE
    Return:
        data_form_station_b
    '''
    data_form_station_c = []
    if ProtocolTemplateFiles.objects.filter(station__stationName__exact = 'Station C', protocolTemplateBeUsed__exact = True).exists():
        protocols = ProtocolTemplateFiles.objects.filter(station__stationName__exact = 'Station C', protocolTemplateBeUsed__exact = True).order_by('protocolStationNumber')
        for protocol in protocols:
            data_form_station_c.append(get_protocol_data_for_form(protocol))
    return data_form_station_c

def extract_data_from_request_protocol (request):
    '''
    Description:
        The function extract the user form data and define a dictionnary with the values
    Input:
        request     # contains the user form data
    Functions:
        get_defined_parameters_protocol_template # located at this file
    Constants:

    Return:
        parameter_values
    '''
    parameter_values = {}
    template_id = request.POST['template_id']
    parameter_names = get_defined_parameters_protocol_template (template_id)
    for parameter in parameter_names :
        parameter_values[parameter] = request.POST[parameter]

    return parameter_values

def get_template_file_name(template_id):
    '''
    Description:
        The function get the protocol template file name for the tempalte id
    Input:
        template_id     # id of the template
    Functions:
        get_protocol_template_obj_from_id  # located at this file
    Return:
        template_file_name
    '''

    protocol_template_obj = get_protocol_template_obj_from_id(template_id)
    template_file_name = protocol_template_obj.get_protocol_file_name()
    return template_file_name

def store_protocol_request_parameter_values(protocol_request, parameters ):
        '''
        Description:
            The function store on database the parameter values used when protocol request
            is created.
        Input:
            protocol_request  # protocol request object
            paramters           # dictionary with the values used in protocol
        Functions:
            get_protocol_template_obj_from_id
        Return:
            template_file_name
        '''
        for name, value in parameters.items():
            data = {}
            data['parameterName'] = name
            data['parameterValue'] = value
            data['protocolRequest'] = protocol_request
            new_parameter_value = ProtocolParameterValues.objects.create_parameter_value(data)
        return


def new_build_request_codeID (user, station ) :
    '''
    Description:
        The function build the request codeID by joining the user, station and
        the number of times that this combination is used
    Input :
        user                # user objects
        station             # station used in the protocol
    Return:
        request codeID string
    '''
    num_times = 0
    if ProtocolRequest.objects.filter(stationName__exact = station, userRequestedBy = user).exists():
        num_times = ProtocolRequest.objects.filter(stationName__exact = station, userRequestedBy = user).count()
    station = station.replace(' ', '')
    num_times += 1
    return user.username +'_' + station + '_' +str(num_times)

def extract_protocol_request_form_data_and_save_to_file (request):
    '''
    Description:
        The function collect the request protocol data form and save the information in the file

    Input :
        request                # full data of the form
    Functions:
        extract_data_from_request_protocol  #Located at this file
        build_protocol_request_file_name    #Located at this file
        increase_protocol_file_id           #Located at this file
        store_file_id                       #Located at this file
        get_template_file_name              #Located at this file
        store_protocol_request_parameter_values  #Located at this file
        add_parameters_in_file              #Located at utils.file_utilities
    Return:
        add_result
    '''
    template_id = request.POST['template_id']

    parameters = extract_data_from_request_protocol(request)
    protocol_file_name = build_protocol_request_file_name(request.user.username,template_id)
    protocol_file_id = increase_protocol_file_id()

    new_prot_file_id_obj = store_file_id (protocol_file_id,request.POST['station'], request.POST['protocol'])
    template_file = get_template_file_name(template_id)

    result = add_parameters_in_file (template_file, protocol_file_name,  parameters, protocol_file_id)
    if result != 'True':
        return result, None

    protocol_request_data = {}
    protocol_request_data['user'] = request.user
    protocol_request_data['generatedFile'] = protocol_file_name
    protocol_request_data['protocolID'] = protocol_file_id
    protocol_request_data['station'] = request.POST['station']
    protocol_request_data['usernotes'] = request.POST['usernotes']
    protocol_request_data['template_id'] = template_id
    protocol_request_data['templateProtocolNumber'] = request.POST ['protocol']
    protocol_request_data['requestedCodeID'] = new_build_request_codeID (request.user, request.POST['station'] )

    new_create_protocol_request = ProtocolRequest.objects.create_protocol_request(protocol_request_data)
    store_protocol_request_parameter_values(new_create_protocol_request, parameters)
    return 'True' , new_create_protocol_request
