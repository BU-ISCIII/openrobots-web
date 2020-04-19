from opentrons.models import *


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
