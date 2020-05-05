import datetime, time, re
from openrobots.models import *
from openrobots.openrobots_config import *


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
    if station == 'Station C':
        if RequestForStationC.objects.filter(userRequestedBy = user, usedTemplateFile__typeOfProtocol__protocolTypeName__exact = protocol_type).exists():
            num_times = RequestForStationC.objects.filter(userRequestedBy = user, usedTemplateFile__typeOfProtocol__protocolTypeName__exact = protocol_type).count()
    elif station == 'Station B':
        if RequestForStationB.objects.filter(userRequestedBy = user, usedTemplateFile__typeOfProtocol__protocolTypeName__exact = protocol_type).exists():
            num_times = RequestForStationB.objects.filter(userRequestedBy = user, usedTemplateFile__typeOfProtocol__protocolTypeName__exact = protocol_type).count()

    num_times += 1
    return user.username + protocol_type + station + str(num_times)

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

def get_form_data_creation_run_file():
    '''
    Description:
        The function will get the Labware information used in the form to create the files
    Functions:

    Return:
        form_data
    '''
    form_data = {}
    form_data['mag_plate_data'] = []
    form_data['waste_plate_data'] =[]
    form_data['reagent_labware_data'] = []
    form_data['mm_labware_data'] = []
    form_data['mm_tube_labware_data']  = []
    form_data['pcr_labware_data'] = []
    form_data['elution_labware_data'] = []
    form_data['master_mix_type_data'] =[]
    form_data['buffer_labware_data'] = []
    form_data['destination_labware_data'] = []
    form_data['dest_tube_labware_data'] = []
    form_data['beads_labware_data'] = []
    form_data['plate_labware_data'] =[]
    form_data['lysate_labware_data'] = []

    if MasterMixLabware.objects.all().exists():
        mm_labwares = MasterMixLabware.objects.all().order_by('MasterMixLabwareType')
        for mm_labware in mm_labwares :
            form_data['mm_labware_data'].append(mm_labware.get_mastermix_labware_type())
    if MasterMixTube.objects.all().exists():
        mm_tube_labwares = MasterMixTube.objects.all().order_by('MasterMixTube')
        for mm_tube_labware in mm_tube_labwares :
            form_data['mm_tube_labware_data'] .append(mm_tube_labware.get_mastermix_tube())
    if PCR_plateLabware.objects.all().exists():
        pcr_labwares = PCR_plateLabware.objects.all().order_by('PCR_plateLabwareType')
        for pcr_labware in pcr_labwares :
            form_data['pcr_labware_data'].append(pcr_labware.get_pcr_plate_labware_type())
    if ElutionStationC_Labware.objects.all().exists():
        elution_labwares = ElutionStationC_Labware.objects.all().order_by('elutionHW_type')
        for elution_labware in elution_labwares :
            form_data['elution_labware_data'].append(elution_labware.get_elution_labware_type())
    if MasterMixType.objects.all().exists():
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


    if ProtocolTemplateFiles.objects.filter(station__stationName__iexact = 'Station A').exists():
        form_data['station_a'] = {}
        protocol_types = ['Protocol 1', 'Protocol 2', 'Protocol 3']
        for i in range(len(protocol_types)) :
            if ProtocolTemplateFiles.objects.filter(station__stationName__iexact = 'Station A', protocolName__icontains = protocol_types[i]).exists():
                form_data['station_a'] [i+1]= ProtocolTemplateFiles.objects.get(station__stationName__iexact = 'Station A', protocolName__icontains = protocol_types[i]).get_protocol_file_name()
    if ProtocolTemplateFiles.objects.filter(station__stationName__iexact = 'Station B').exists():
        form_data['station_b'] = ProtocolTemplateFiles.objects.get(station__stationName__iexact = 'Station B').get_protocol_file_name()
    if ProtocolTemplateFiles.objects.filter(station__stationName__iexact = 'Station C').exists():
        form_data['station_c'] = ProtocolTemplateFiles.objects.get(station__stationName__iexact = 'Station C').get_protocol_file_name()

    return form_data

def get_list_labware_inventory():
    '''
    Description:
        The function will get the labware availables and fetch for each inventory data
    Return:
        labware_data
    '''
    labware_data = []
    if Elution_Labware.objects.all().exists():
        elutions = Elution_Labware.objects.all().order_by('brand')
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
    if Elution_Labware.objects.filter(pk__exact = labware_id).exists():
        labware_obj = Elution_Labware.objects.get(pk__exact = labware_id)
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
        protocol_template_obj = ProtocolTemplateFiles.objects.get(protocolTemplateFileName__exact = template)
        protocol_name = protocol_template_obj.get_protocol_name()
        try:
            prot = re.search(r'.*Station [A|B|C] Protocol (\d).*',protocol_name).group(1)
        except:
            prot = '1'

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


def extract_form_data_station (request) :
    '''
    Description:
        The function extract the user form data and define a dictionnary with the values
    Constants:
        PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_C
        PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_B
        PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_A_PROT_1
        PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_A_PROT_2
        PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_A_PROT_3
    Return:
        valid_metadata
    '''
    data_for_file = {}
    data_for_file2 = {}
    data_for_database = {}
    if request.POST['station'] == 'Station C':
        for item in PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_C:
            data_for_file[item] = request.POST[item]
        #[(data_for_file2[item] = request.POST[item]) for item in PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_C ]
        for item in MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_C :
            data_for_database[item[1]] = request.POST[item[0]]

        data_for_database['station'] = request.POST['station']
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
    # get request for Station C protocols
    if RequestForStationC.objects.all().exists():
        request_list['station_c'] = []
        c_requests = RequestForStationC.objects.all().order_by('userRequestedBy').order_by('generatedat')
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


    return request_list

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
