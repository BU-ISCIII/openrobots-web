import os
from django.conf import settings
##### Allow to import the configuration samba files from configuration folder
import sys
sys.path.append('../')


############## FOLDER SETTINGS ###############################
## Directory settings for processing the run data files ######
## Relative path from settings.BASE_DIR

## Relative path from settings.MEDIA_ROOT
OPENROBOTS_TEMPLATE_DIRECTORY = 'templates'
OPENROBOTS_OUTPUT_DIRECTORY = 'protocol_files'
OPENROBOTS_MODULE_TYPE_GUIDES_DIRECTORY = 'user-guide'
OPENROBOTS_LABWARE_JSON_DIRECTORY = 'labware_inventory/json'
OPENROBOTS_LABWARE_PYTHON_DIRECTORY = 'labware_inventory/python'
OPENROBOTS_LABWARE_IMAGE_DIRECTORY = 'labware_inventory/image'

#OPENROBOTS_TEMPLATE_FILE_NAME = 'v1_station_c_S3.ot2.apiv2.py'
PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_A = ['NUM_SAMPLES' , 'MM_LABWARE','MMTUBE_LABWARE', 'PCR_LABWARE', 'ELUTION_LABWARE',
            'PREPARE_MASTERMIX', 'TRANSFER_MASTERMIX', 'TRANSFER_SAMPLES', 'MM_TYPE']
PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_B = ['NUM_SAMPLES']

PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_C = ['NUM_SAMPLES' , 'MM_LABWARE','MMTUBE_LABWARE', 'PCR_LABWARE', 'ELUTION_LABWARE',
            'PREPARE_MASTERMIX', 'TRANSFER_MASTERMIX', 'TRANSFER_SAMPLES', 'MM_TYPE']

MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_C = [('NUM_SAMPLES','numberOfSamples') , ('MM_LABWARE','masterMixLabware'),('MMTUBE_LABWARE','masterMixTubeLabware'),
        ('PCR_LABWARE','pcrPlateLabware'), ('ELUTION_LABWARE','elutionLabware'), ('PREPARE_MASTERMIX','prepareMastermix'),
        ('TRANSFER_MASTERMIX','transferMastermix'), ('TRANSFER_SAMPLES','transferSamples'), ('MM_TYPE','masterMixType')]
OPENROBOTS_DELIMITATION_PARAMETERS_TAGS = ['# Parameters to adapt the protocol',
                    '# End Parameters to adapt the protocol']

JSON_LABWARE_ROOT_FIELDS_TO_CHECK = ['metadata', 'dimensions','wells','parameters','brand']
JSON_LABWARE_FIELDS_TO_GET = {'brand':['brand'],'metadata':['displayName','displayCategory'],'dimensions':['xDimension',
        'yDimension', 'zDimension'],'parameters':['isMagneticModuleCompatible', 'loadName']}
JSON_LABWARE_WELL_TO_GET ={'wells':{'A1':['depth','totalLiquidVolume','shape', 'diameter','x','y','z']}}

INVALID_TEMPLATE_FILE = ['Invalid Protocol File ', 'Delimitation Parameters tags are not included in file']
INVALID_JSON_FILE = ['Invalid json File', 'File does not contains all requested information']

METADATA_FIELDS_FOR_PROTOCOL_TEMPLATE = ['protocolName', 'author', 'source','apiLevel']
PROTOCOL_STEPS_IN_TEMPLATE_FILE = ['prepare_mastermix', 'transfer_mastermix' , 'transfer_samples' ]
ADMIN_USERS = ['admin']
