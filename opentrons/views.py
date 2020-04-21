from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from opentrons.utils.fetching_information import  *
from opentrons.utils.file_utilities import  *

def index(request):
    #
    return redirect ('/createProtocolFile')
    return render(request, 'opentrons/index.html')
@login_required
def create_protocol_file(request):
    # Get data to display in form
    '''
    parameter = {}
    parameter['NUM_SAMPLES'] = '96'
    parameter['MM_LABWARE'] = '\'opentrons aluminum block\''
    parameter['MMTUBE_LABWARE'] = '\'2ml tubes\''
    parameter['PCR_LABWARE'] = '\'opentrons aluminum nest plate\''
    parameter['ELUTION_LABWARE'] = '\'opentrons aluminum nest plate\''
    parameter['PREPARE_MASTERMIX'] = 'True'
    parameter['MM_TYPE'] = '\'MM1\''
    parameter['TRANSFER_MASTERMIX'] = 'True'
    parameter['TRANSFER_SAMPLES'] = 'True'
    #import pdb; pdb.set_trace()
    #add_parameters_in_file(parameter)
    '''
    form_data = get_form_data_creation_run_file()
    if request.method == 'POST' and (request.POST['action']=='createprotocolfile'):
        template = request.POST['template']

        parameters, database = extract_form_data(request)
        protocol_type = get_protocol_type_from_template(template)
        protocol_file = build_protocol_file_name(request.user.username,template)

        add_result = add_parameters_in_file (template, protocol_file,  parameters)
        if add_result != 'True':
            return render(request, 'opentrons/createProtocolFile.html' ,{'form_data': form_data, 'error': add_result})
        database['generatedFile'] = protocol_file
        database['requestedCodeID'] = build_request_codeID (request.user, protocol_type, request.POST['station'] )
        new_create_protocol = RequestOpenTronsFiles.objects.create_new_request(database)

        display_result = new_create_protocol.get_result_data()


        return render(request, 'opentrons/createProtocolFile.html' ,{'display_result': display_result})
    else:
        return render(request, 'opentrons/createProtocolFile.html' ,{'form_data': form_data})

def display_template_file(request, p_template_id):


    protocol_template_data = get_protocol_template_information(p_template_id)

    return render(request, 'opentrons/displayTemplateFile.html' ,{'protocol_template_data': protocol_template_data})

@login_required
def detail_robot_inventory(request,robot_id):
    robot_inventory_data = get_robot_inventory_data(robot_id)
    return render(request, 'opentrons/detailRobotInventory.html' ,{'robot_inventory_data': robot_inventory_data} )

@login_required
def robot_inventory(request):
    robot_list_inventory = get_list_robot_inventory()

    return render(request, 'opentrons/robotInventory.html' ,{'robot_list_inventory': robot_list_inventory} )

@login_required
def upload_protocol_templates(request):
    if request.user.username not in ADMIN_USERS :
        return render(request, 'opentrons/index.html')
    template_data = {}
    template_data['protocol_types'] = get_protocol_types()
    template_data['stations'] = get_stations_names()
    stored_protocol_file= get_stored_protocols_files()
    if request.method == 'POST' and request.POST['action'] == 'addtemplatefile':
        ## fetch the file from user form and  build the file name  including
        ## the date and time on now to store in database
        file_name = request.FILES['newtemplatefile'].name
        saved_file , file_name = store_protocol_template_file(request.FILES['newtemplatefile'])

        ## get the libary name to check if it is already defined
        if not template_file_valid_format(saved_file):
            error_message = INVALID_TEMPLATE_FILE
            os.remove(saved_file)
            return render(request, 'opentrons/uploadProtocolTemplates.html', {'error_message': error_message ,
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



        #import pdb; pdb.set_trace()
        return render(request, 'opentrons/uploadProtocolTemplates.html' , {'template_data': template_data ,'stored_protocol_file': stored_protocol_file,
                                'created_new_file': created_new_file  })
    else:
        return render(request, 'opentrons/uploadProtocolTemplates.html' , {'template_data': template_data, 'stored_protocol_file': stored_protocol_file})
