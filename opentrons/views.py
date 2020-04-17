from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from opentrons.utils.fetching_information import  *
from opentrons.utils.file_utilities import  *

def index(request):
    #
    return render(request, 'opentrons/index.html')
@login_required
def request_file(request):
    # Get data to display in form
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
    add_parameters_in_file(parameter)
    form_data = get_form_data_creation_run_file()
    if request.method == 'POST' and (request.POST['action']=='createfile'):
        import pdb; pdb.set_trace()
        '''
        transfersamples
        transfermaxtermix
        preparemaxtermix
        elution
        pcrplate
        mmtype
        mmtube
        mmlabware
        samples
        station
        '''
        return render(request, 'opentrons/requestFile.html' ,{'form_data': form_data})
    else:
        return render(request, 'opentrons/requestFile.html' ,{'form_data': form_data})
