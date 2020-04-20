import datetime, time
from opentrons.models import *
from opentrons.opentrons_config import *


def  build_protocol_file_name(user, template):
    '''
    Description:
        The function build the protocol file name by joining the user, protocol_type, station and time
    Functions:
        get_protocol_type_from_template   # located at this file
        get_station_from_template           # located at this file
    Return:
        protocol_file_name
    '''
    name = [user]
    name.append(''.join(get_protocol_type_from_template(template).split()))
    name.append(''.join(get_station_from_template(template).split()))
    name.append(time.strftime("%Y%m%d-%H%M%S"))

    return '_'.join(name) + '.py'

def build_request_codeID (user, protocol_type, station ) :
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
    if RequestOpenTronsFiles.objects.filter(userRequestedBy = user, usedTemplateFile__typeOfProtocol__protocolTypeName__exact = protocol_type, station__stationName__exact = station).exists():
        num_times = RequestOpenTronsFiles.objects.filter(userRequestedBy = user, usedTemplateFile__typeOfProtocol__protocolTypeName__exact = protocol_type, station__stationName__exact = station).count()
    num_times += 1
    return user.username + protocol_type + station + str(num_times)

def get_form_data_creation_run_file():
    '''
    Description:
        The function will get the Labware information used in the form to create the files
    Functions:

    Return:
        form_data
    '''
    form_data = {}
    mm_labware_data = []
    mm_tube_labware_data = []
    pcr_labware_data = []
    elution_labware_data = []
    master_mix_type_data = []

    if MasterMixLabware.objects.all().exists():
        mm_labwares = MasterMixLabware.objects.all().order_by('MasterMixLabwareType')
        for mm_labware in mm_labwares :
            mm_labware_data.append(mm_labware.get_mastermix_labware_type())
    if MasterMixTube.objects.all().exists():
        mm_tube_labwares = MasterMixTube.objects.all().order_by('MasterMixTube')
        for mm_tube_labware in mm_tube_labwares :
            mm_tube_labware_data.append(mm_tube_labware.get_mastermix_tube())
    if PCR_plateLabware.objects.all().exists():
        pcr_labwares = PCR_plateLabware.objects.all().order_by('PCR_plateLabwareType')
        for pcr_labware in pcr_labwares :
            pcr_labware_data.append(pcr_labware.get_pcr_plate_labware_type())
    if Elution_Labware.objects.all().exists():
        elution_labwares = Elution_Labware.objects.all().order_by('elutionHW_type')
        for elution_labware in elution_labwares :
            elution_labware_data.append(elution_labware.get_elution_labware_type())
    if MasterMixType.objects.all().exists():
        master_mix_types = MasterMixType.objects.all().order_by('MasterMixType')
        for master_mix_type in master_mix_types :
            master_mix_type_data.append(master_mix_type.get_master_mix_type())
    form_data['mm_labware_data'] = mm_labware_data
    form_data['mm_tube_labware_data'] = mm_tube_labware_data
    form_data['pcr_labware_data'] = pcr_labware_data
    form_data['elution_labware_data'] = elution_labware_data
    form_data['master_mix_type_data'] = master_mix_type_data
    if ProtocolTemplateFiles.objects.filter(station__stationName__iexact = 'Station A').exists():
        form_data['station_a'] = ProtocolTemplateFiles.objects.get(station__stationName__iexact = 'Station A').get_protocol_file_name()
    if ProtocolTemplateFiles.objects.filter(station__stationName__iexact = 'Station B').exists():
        form_data['station_b'] = ProtocolTemplateFiles.objects.get(station__stationName__iexact = 'Station B').get_protocol_file_name()
    if ProtocolTemplateFiles.objects.filter(station__stationName__iexact = 'Station C').exists():
        form_data['station_c'] = ProtocolTemplateFiles.objects.get(station__stationName__iexact = 'Station C').get_protocol_file_name()

    return form_data

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
        protocol_data['functions'] = p_template.get_functions()
    return protocol_data


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

def get_station_from_template(template):
    '''
    Description:
        The function will fetch the station name from protocol template
    Return:
        station name
    '''
    if ProtocolTemplateFiles.objects.filter(protocolTemplateFileName__exact = template).exists() :
        return ProtocolTemplateFiles.objects.get(protocolTemplateFileName__exact = template).get_station()
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

def get_stored_protocols_files():
    '''
    Description:
        The function get the main information for the protocols templates defined
    Return:
        protocol_file_data
    '''
    protocol_file_data = []

    if ProtocolTemplateFiles.objects.all().exists():
        p_templates = ProtocolTemplateFiles.objects.all().order_by('station')
        for p_template in p_templates :
            protocol_file_data.append(p_template.get_main_data())
    return protocol_file_data


def extract_form_data (request) :
    '''
    Description:
        The function extract the user form data and define a dictionnary with the values
    Constants:
        PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_C
    Return:
        valid_metadata
    '''
    if request.POST['station'] == 'Station C':
        data_for_file = {}
        data_for_file2 = {}
        data_for_database = {}
        for item in PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_C:
            data_for_file[item] = request.POST[item]
        #[(data_for_file2[item] = request.POST[item]) for item in PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_C ]
        for item in MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_C :
            data_for_database[item[1]] = request.POST[item[0]]
    # Add common data to store on database
    data_for_database['station'] = request.POST['station']
    data_for_database['usedTemplateFile'] = request.POST['template']
    data_for_database['userNotes'] = request.POST['usernotes']
    data_for_database['userRequestedBy'] = request.user

    return data_for_file , data_for_database



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
