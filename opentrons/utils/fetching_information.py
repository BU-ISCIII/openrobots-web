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
