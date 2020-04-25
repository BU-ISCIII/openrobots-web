from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from openrobots.utils.fetching_information import  *
from openrobots.utils.file_utilities import  *
from openrobots.openrobots_config import *

def index(request):
    #
    #return redirect ('/createProtocolFile')
    return render(request, 'openrobots/index.html')
@login_required
def create_protocol_file(request):
    # Get data to display in form
    form_data = get_form_data_creation_run_file()
    if request.method == 'POST' and (request.POST['action']=='createprotocolfile'):
        template = request.POST['template']

        parameters, database = extract_form_data(request)
        protocol_type = get_protocol_type_from_template(template)
        protocol_file = build_protocol_file_name(request.user.username,template)

        add_result = add_parameters_in_file (template, protocol_file,  parameters)
        if add_result != 'True':
            return render(request, 'openrobots/createProtocolFile.html' ,{'form_data': form_data, 'error': add_result})
        database['generatedFile'] = protocol_file
        database['requestedCodeID'] = build_request_codeID (request.user, protocol_type, request.POST['station'] )
        new_create_protocol = RequestOpenTronsFiles.objects.create_new_request(database)

        display_result = new_create_protocol.get_result_data()


        return render(request, 'openrobots/createProtocolFile.html' ,{'display_result': display_result})
    else:
        return render(request, 'openrobots/createProtocolFile.html' ,{'form_data': form_data})


@login_required
def define_labware(request) :
    form_data = get_elution_hw_types()
    if request.method == 'POST' and (request.POST['action']=='definelabware'):
        json_saved_file , json_file_name = store_user_file(request.FILES['jsonfile'], OPENTRONS_LABWARE_JSON_DIRECTORY )

        if not json_file_valid_format(json_saved_file):
            error_message = INVALID_JSON_FILE
            os.remove(json_saved_file)
            return render(request, 'openrobots/defineLabware.html' ,{'form_data': form_data, 'error_message': error_message})

        json_dict = json_get_labware_information(json_saved_file)
        json_dict['elutionhwtype'] = request.POST['elutionhwtype']
        #json_dict['labwarename'] = request.POST['labwarename']
        json_dict['jsonFile'] = json_file_name

        if 'pythonfile' in request.FILES :
            python_saved_file , python_file_name = store_user_file(request.FILES['pythonfile'], OPENTRONS_LABWARE_PYTHON_DIRECTORY )
            json_dict['pythonFile'] = python_file_name
        else:
            json_dict['pythonFile'] = ''

        if 'imagefile' in request.FILES :
            image_saved_file , image_file_name = store_user_file(request.FILES['imagefile'], OPENTRONS_LABWARE_IMAGE_DIRECTORY )
            json_dict['imageFile'] = image_file_name
        else:
            json_dict['imageFile'] = ''

        new_elution_labware = Elution_Labware.objects.create_elution_labware(json_dict)
        created_new_labware = new_elution_labware.get_minimun_elution_lab_data()
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
def upload_protocol_templates(request):
    if request.user.username not in ADMIN_USERS :
        return render(request, 'openrobots/index.html')
    template_data = {}
    template_data['protocol_types'] = get_protocol_types()
    template_data['stations'] = get_stations_names()
    stored_protocol_file= get_stored_protocols_files()
    if request.method == 'POST' and request.POST['action'] == 'addtemplatefile':
        ## fetch the file from user form and  build the file name  including
        ## the date and time on now to store in database
        file_name = request.FILES['newtemplatefile'].name
        saved_file , file_name = store_user_file(request.FILES['newtemplatefile'],OPENTRONS_TEMPLATE_DIRECTORY )

        ## get the libary name to check if it is already defined
        if not template_file_valid_format(saved_file):
            error_message = INVALID_TEMPLATE_FILE
            os.remove(saved_file)
            return render(request, 'openrobots/uploadProtocolTemplates.html', {'error_message': error_message ,
                        'stored_protocol_file': stored_protocol_file, 'template_data': template_data} )
        protocol_file_data = {}
        protocol_file_data = get_metadata_from_file(saved_file)
        protocol_file_data.update(get_steps_used_in_protocol(saved_file))
        protocol_file_data['station'] = request.POST['station']
        protocol_file_data['typeOfProtocol'] = request.POST['protocoltype']
        protocol_file_data['file_name'] = file_name
        protocol_file_data['user'] = request.user
        new_protocol_template = ProtocolTemplateFiles.objects.create_protocol_template(protocol_file_data)
        created_new_file = {}
        created_new_file['protocol_name'] = request.POST['protocoltype']
        created_new_file['file_name'] = request.FILES['newtemplatefile'].name

        return render(request, 'openrobots/uploadProtocolTemplates.html' , {'template_data': template_data ,'stored_protocol_file': stored_protocol_file,
                                'created_new_file': created_new_file  })
    else:
        return render(request, 'openrobots/uploadProtocolTemplates.html' , {'template_data': template_data, 'stored_protocol_file': stored_protocol_file})
