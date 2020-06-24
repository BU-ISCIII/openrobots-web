from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from openrobots.utils.fetching_information import  *
from openrobots.utils.file_utilities import  *
from openrobots.openrobots_config import *
import json

def index(request):
    #
    #return redirect ('/createProtocolFile')
    return render(request, 'openrobots/index.html')


@login_required
def create_pcr_protocol_file(request):
    # Get data to display in form
    form_data = get_form_data_creation_run_file()

    if request.method == 'POST' and (request.POST['action']=='createprotocolfile'):
        template = request.POST['template']

        parameters, database = extract_form_data_station(request)
        protocol_type = get_protocol_type_from_template(template)
        protocol_file = build_protocol_file_name(request.user.username,template)
        protocol_file_id = increase_protocol_file_id()
        new_prot_file_id_obj = store_file_id (protocol_file_id,request.POST['station'], request.POST['protocol'])

        add_result = add_parameters_in_file (template, protocol_file,  parameters, protocol_file_id)
        if add_result != 'True':
            return render(request, 'openrobots/createPCRProtocolFile.html' ,{'form_data': form_data, 'error': add_result})
        database['generatedFile'] = protocol_file
        database['protocolID'] = protocol_file_id
        database['requestedCodeID'] = build_request_codeID (request.user, protocol_type, request.POST['station'],request.POST['protocol'] )

        if request.POST['station'] == 'Station C':
            if request.POST['protocol'] == '1':
                new_create_protocol = RequestForStationC_Prot1.objects.create_new_request(database)
            else:
                new_create_protocol = RequestForStationC_Prot2.objects.create_new_request(database)
        else:
            return render(request, 'openrobots/createPCRProtocolFile.html' ,{'form_data': form_data})

        display_result = new_create_protocol.get_result_data()
        return render(request, 'openrobots/createPCRProtocolFile.html' ,{'display_result': display_result})
    else:
        return render(request, 'openrobots/createPCRProtocolFile.html' ,{'form_data': form_data})

@login_required
def create_extraction_protocol_file(request):
    form_data = get_form_data_creation_run_file()
    if request.method == 'POST' and (request.POST['action']=='createprotocolfile'):
        template = request.POST['template']

        parameters, database = extract_form_data_station(request)
        protocol_type = get_protocol_type_from_template(template)
        protocol_file = build_protocol_file_name(request.user.username,template)

        protocol_file_id = increase_protocol_file_id()
        new_prot_file_id_obj = store_file_id (protocol_file_id,request.POST['station'], request.POST['protocol'])

        add_result = add_parameters_in_file (template, protocol_file,  parameters, protocol_file_id)
        if add_result != 'True':
            return render(request, 'openrobots/createExtractionProtocolFile.html' ,{'form_data': form_data, 'error': add_result})
        database['generatedFile'] = protocol_file
        database['protocolID'] = protocol_file_id
        database['requestedCodeID'] = build_request_codeID (request.user, protocol_type, request.POST['station'], request.POST['protocol'] )
        if request.POST['station'] == 'Station B':
            new_create_protocol = RequestForStationB.objects.create_new_request(database)
        elif  request.POST['station'] == 'Station A' and request.POST['protocol'] == '1' :
            new_create_protocol = RequestForStationA_Prot1.objects.create_new_request(database)
        elif  request.POST['station'] == 'Station A' and request.POST['protocol'] == '2' :
            new_create_protocol = RequestForStationA_Prot2.objects.create_new_request(database)
        elif  request.POST['station'] == 'Station A' and request.POST['protocol'] == '3' :
            new_create_protocol = RequestForStationA_Prot3.objects.create_new_request(database)
        else:
            return render(request, 'openrobots/createExtractionProtocolFile.html' ,{'form_data': form_data})

        display_result = new_create_protocol.get_result_data()
        return render(request, 'openrobots/createExtractionProtocolFile.html' ,{'display_result': display_result})

    return render(request, 'openrobots/createExtractionProtocolFile.html' ,{'form_data': form_data})

@login_required
def define_labware(request) :
    form_data = get_elution_hw_types()
    if request.method == 'POST' and (request.POST['action']=='definelabware'):
        json_saved_file , json_file_name = store_user_file(request.FILES['jsonfile'], OPENROBOTS_LABWARE_JSON_DIRECTORY )

        if not json_file_valid_format(json_saved_file):
            error_message = INVALID_JSON_FILE
            os.remove(json_saved_file)
            return render(request, 'openrobots/defineLabware.html' ,{'form_data': form_data, 'error_message': error_message})

        json_dict = json_get_labware_information(json_saved_file)

        json_dict['jsonFile'] = json_file_name

        if 'pythonfile' in request.FILES :
            python_saved_file , python_file_name = store_user_file(request.FILES['pythonfile'], OPENROBOTS_LABWARE_PYTHON_DIRECTORY )
            json_dict['pythonFile'] = python_file_name
        else:
            json_dict['pythonFile'] = ''

        if 'imagefile' in request.FILES :
            image_saved_file , image_file_name = store_user_file(request.FILES['imagefile'], OPENROBOTS_LABWARE_IMAGE_DIRECTORY )
            json_dict['imageFile'] = image_file_name
        else:
            json_dict['imageFile'] = ''

        new_inventory_labware = InventoryLabware.objects.create_inventory_labware(json_dict)
        created_new_labware = new_inventory_labware.get_minimun_elution_lab_data()
        ## remove the id value in the data
        del created_new_labware[-1]
        return render(request, 'openrobots/defineLabware.html' ,{'created_new_labware': created_new_labware})
    else:
        return render(request, 'openrobots/defineLabware.html' ,{'form_data': form_data})

@login_required
def define_robot (request):

    robot_inventory_form_data = get_form_data_creation_new_robot()

    if request.method == 'POST' and (request.POST['action']=='definerobot'):
        robot_data = extract_define_robot_form_data(request)
        robot_data['userName'] = request.user
        new_robot = RobotsInventory.objects.create_robot(robot_data)
        for module in robot_data['modules']:
            new_robot.set_module(get_module_obj_from_id (module))

        created_new_robot = new_robot.get_minimum_robot_data()
        return render(request, 'openrobots/defineRobot.html' ,{'created_new_robot': created_new_robot})
    return render(request, 'openrobots/defineRobot.html' ,{'robot_inventory_form_data': robot_inventory_form_data})


@login_required
def display_template_file(request, p_template_id):
    protocol_template_data = get_protocol_template_information(p_template_id)

    return render(request, 'openrobots/displayTemplateFile.html' ,{'protocol_template_data': protocol_template_data})

@login_required
def detail_labware_inventory(request,labware_id):
    labware_inventory_data = get_labware_inventory_data(labware_id)
    return render(request, 'openrobots/detailLabwareInventory.html' ,{'labware_inventory_data': labware_inventory_data} )

@login_required
def detail_module_inventory(request, module_id):
    module_inventory_data = get_module_inventory_data(module_id)
    return render(request, 'openrobots/detailModuleInventory.html' ,{'module_inventory_data': module_inventory_data} )

@login_required
def detail_robot_inventory(request,robot_id):
    robot_inventory_data = get_robot_inventory_data(robot_id)
    return render(request, 'openrobots/detailRobotInventory.html' ,{'robot_inventory_data': robot_inventory_data} )

@login_required
def labware_inventory(request):
    labware_list_inventory = get_list_labware_inventory()
    return render(request, 'openrobots/labwareInventory.html', {'labware_list_inventory': labware_list_inventory})

@login_required
def modules_inventory(request):
    module_list_inventory = get_list_module_inventory()
    return render(request, 'openrobots/modulesInventory.html', {'module_list_inventory': module_list_inventory})


@login_required
def robot_inventory(request):
    robot_list_inventory = get_list_robot_inventory()
    return render(request, 'openrobots/robotInventory.html' ,{'robot_list_inventory': robot_list_inventory} )

@login_required
def list_of_requests(request):
    list_requests_data = get_list_of_requests()
    return render(request, 'openrobots/listOfRequests.html' ,{'list_requests_data': list_requests_data} )


@login_required
def robots_jobs (request):
    form_data = get_form_data_robots_usage()

    if request.method == 'POST' and request.POST['action'] == 'robotsjobs':
        start_date=request.POST['startdate']
        end_date=request.POST['enddate']
        if start_date != '':
            if not check_valid_date_format(start_date) :
                error_message = ERROR_INVALID_FORMAT_FOR_DATES
                return render(request, 'openrobots/robotsJobs.html', {'error_message':error_message})
        if end_date != '':
            if not check_valid_date_format(end_date) :
                error_message = ERROR_INVALID_FORMAT_FOR_DATES
                return render(request, 'openrobots/robotsJobs.html', {'error_message':error_message})

        robots_action_objs = get_robots_action_from_user_form(request.POST)

        if not robots_action_objs:
            error_message = ERROR_NOT_ROBOT_ACTION_MATCHES_FOUND
            return render (request, 'openrobots/robotsJobs.html', {'error_message':error_message, 'form_data': form_data})

        display_robot_utilization = get_robots_information_utilization (robots_action_objs)
        #import pdb; pdb.set_trace()
        return render (request, 'openrobots/robotsJobs.html',{'display_robot_utilization': display_robot_utilization})

    return render (request, 'openrobots/robotsJobs.html',{'form_data': form_data})

@login_required
def detail_action_robot(request, action_id):
    if robot_action_exists(action_id):
        detail_data = get_action_robot_detail(action_id)
        return render (request, 'openrobots/detailActionRobot.html',{'detail_data':detail_data})


    return redirect ('/')

@login_required
def upload_protocol_templates(request):
    if request.user.username not in ADMIN_USERS :
        return render(request, 'openrobots/index.html')

    if request.method == 'POST' and request.POST['action'] == 'addtemplatefile':
        ## fetch the file from user form and  build the file name  including
        ## the date and time on now to store in database
        file_name = request.FILES['newtemplatefile'].name
        saved_file , file_name = store_user_file(request.FILES['newtemplatefile'],OPENROBOTS_TEMPLATE_DIRECTORY )

        ## get the libary name to check if it is already defined
        if not template_file_valid_format(saved_file):
            error_message = INVALID_TEMPLATE_FILE
            os.remove(saved_file)
            template_data = {}
            template_data['protocol_types'] = get_protocol_types()
            template_data['stations'] = get_stations_names()
            return render(request, 'openrobots/uploadProtocolTemplates.html', {'error_message': error_message ,
                        'template_data': template_data} )
        protocol_file_data = {}
        protocol_file_data = get_metadata_from_file(saved_file)
        protocol_file_data.update(get_steps_used_in_protocol(saved_file))
        protocol_file_data['station'] = request.POST['station']
        protocol_file_data['typeOfProtocol'] = request.POST['protocoltype']
        protocol_file_data['file_name'] = file_name
        protocol_file_data['user'] = request.user
        new_protocol_template = ProtocolTemplateFiles.objects.create_protocol_template(protocol_file_data)



        #return render(request, 'openrobots/uploadProtocolTemplates.html' , {'template_data': template_data ,'stored_protocol_file': stored_protocol_file,
        #                            'created_new_file': created_new_file  })

        define_parameter = get_form_data_define_parameter()
        define_parameter['protocol_template_id'] = new_protocol_template.get_protocol_template_id()
        return render(request, 'openrobots/uploadProtocolTemplates.html' , {'define_parameter': define_parameter  })

    elif request.method == 'POST' and request.POST['action'] == 'defineParameter':

        define_parameter_data, valid_parameters = get_input_define_parameter(request.POST)
        if not valid_parameters:
            define_parameter = get_form_data_define_parameter()
            define_parameter['parameter_values'] = json.loads(request.POST['parameter_data'])
            define_parameter['protocol_template_id'] = request.POST['protocol_template_id']
            return render(request, 'openrobots/uploadProtocolTemplates.html' , {'define_parameter': define_parameter  })
        protocol_template_id = request.POST['protocol_template_id']
        store_define_parameter(define_parameter_data, protocol_template_id )
        # Update template file with paramteres defined
        set_protocol_parameters_defined(protocol_template_id)
        created_new_file = get_recorded_protocol_template(protocol_template_id)
        return render(request, 'openrobots/uploadProtocolTemplates.html' , {'created_new_file': created_new_file  })

    elif request.method == 'POST' and request.POST['action'] == 'addParameter':

        define_parameter = get_form_data_define_parameter()
        define_parameter['protocol_template_id'] = request.POST['protocol_template_id']
        return render(request, 'openrobots/uploadProtocolTemplates.html' , {'define_parameter': define_parameter  })
    else:
        template_data = {}
        template_data['protocol_types'] = get_protocol_types()
        template_data['stations'] = get_stations_names()
        stored_protocol_file= get_stored_protocols_files()
        pending_protocols = get_pending_protocol_parameters()
        return render(request, 'openrobots/uploadProtocolTemplates.html' , {'template_data': template_data, 'stored_protocol_file': stored_protocol_file,
                                'pending_protocols': pending_protocols})
