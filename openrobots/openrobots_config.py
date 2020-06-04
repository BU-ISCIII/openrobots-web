import os
from django.conf import settings
##### Allow to import the configuration samba files from configuration folder
import sys
sys.path.append('../')

try:
    from .url_configuration import DOMAIN_SERVER
except:
    DOMAIN_SERVER = 'localhost'


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

PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_A_PROT_1 = ['NUM_SAMPLES' , 'BUFFER_LABWARE','DESTINATION_LABWARE', 'DEST_TUBE', 'LANGUAGE','RESET_TIPCOUNT', 'VOLUME_BUFFER']
PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_A_PROT_2 = ['NUM_SAMPLES' , 'BEADS_LABWARE','PLATE_LABWARE','LANGUAGE', 'RESET_TIPCOUNT', 'DILUTE_BEADS', 'VOLUME_BEADS']
PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_A_PROT_3 = ['NUM_SAMPLES' , 'LYSATE_LABWARE','PLATE_LABWARE','LANGUAGE', 'RESET_TIPCOUNT', 'VOLUME_LYSATE', 'BEADS']

PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_B = ['NUM_SAMPLES', 'REAGENT_LABWARE','MAGPLATE_LABWARE', 'WASTE_LABWARE', 'ELUTION_LABWARE','LANGUAGE',
            'RESET_TIPCOUNT', 'DISPENSE_BEADS', 'REUSE_TIPS']

PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_C_PROT_1 = ['NUM_SAMPLES' , 'MM_LABWARE','MMTUBE_LABWARE', 'PCR_LABWARE', 'ELUTION_LABWARE', 'LANGUAGE', 'VOLUME_ELUTION',
            'PREPARE_MASTERMIX', 'RESET_TIPCOUNT', 'TRANSFER_MASTERMIX', 'TRANSFER_SAMPLES', 'MM_TYPE']
PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_C_PROT_2 = ['NUM_SAMPLES' , 'MM_LABWARE', 'PCR_LABWARE', 'ELUTION_LABWARE', 'LANGUAGE', 'VOLUME_ELUTION','RESET_TIPCOUNT']

MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_A_PROT_1 = [('NUM_SAMPLES','numberOfSamples') ,('BUFFER_LABWARE','bufferLabware'),('DESTINATION_LABWARE', 'destinationLabware'),
        ('DEST_TUBE', 'destinationTube'), ('LANGUAGE','languageCode'), ('RESET_TIPCOUNT', 'resetTipcount'),  ('VOLUME_BUFFER','volumeBuffer')]

MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_A_PROT_2 = [('NUM_SAMPLES','numberOfSamples') ,('BEADS_LABWARE','beadsLabware'),('PLATE_LABWARE', 'plateLabware'),
        ('LANGUAGE','languageCode'), ('RESET_TIPCOUNT', 'resetTipcount'), ('DILUTE_BEADS', 'diluteBeads'), ('VOLUME_BEADS', 'volumeBeads')]

MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_A_PROT_3 = [('NUM_SAMPLES','numberOfSamples') ,('LYSATE_LABWARE','lysateLabware'),('PLATE_LABWARE', 'plateLabware'),
        ('LANGUAGE','languageCode'), ('VOLUME_LYSATE', 'volumeLysate'),  ('RESET_TIPCOUNT', 'resetTipcount'), ('BEADS','beads')]

MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_B = [('NUM_SAMPLES','numberOfSamples') ,('REAGENT_LABWARE','reagentLabware'),('MAGPLATE_LABWARE', 'magPlateLabware'),
        ('WASTE_LABWARE', 'wasteLabware'), ('LANGUAGE','languageCode'), ('ELUTION_LABWARE','elutionLabware'),('DISPENSE_BEADS', 'dispenseBeads'),
        ('RESET_TIPCOUNT', 'resetTipcount'), ('REUSE_TIPS', 'reuseTips') ]

MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_C_PROT_1 = [('NUM_SAMPLES','numberOfSamples') , ('MM_LABWARE','masterMixLabware'),('MMTUBE_LABWARE','masterMixTubeLabware'),
        ('PCR_LABWARE','pcrPlateLabware'), ('ELUTION_LABWARE','c_elution_Labware'), ('LANGUAGE','languageCode'), ('VOLUME_ELUTION', 'volumeElution'),
        ('PREPARE_MASTERMIX','prepareMastermix'),  ('RESET_TIPCOUNT', 'resetTipcount'), ('TRANSFER_MASTERMIX','transferMastermix'),
        ('TRANSFER_SAMPLES','transferSamples'), ('MM_TYPE','masterMixType')]

MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_C_PROT_2 = [('NUM_SAMPLES','numberOfSamples') , ('MM_LABWARE','masterMixLabware'),
        ('PCR_LABWARE','pcrPlateLabware'), ('ELUTION_LABWARE','c_elution_Labware'), ('LANGUAGE','languageCode'), ('VOLUME_ELUTION', 'volumeElution'),
        ('RESET_TIPCOUNT', 'resetTipcount')]

OPENROBOTS_DELIMITATION_PARAMETERS_TAGS = ['# Parameters to adapt the protocol',
                    '# End Parameters to adapt the protocol']

DOMAIN_SERVER_CONFIGURATION_FILE_HEADING = '############# DOMAIN SERVER CONFIGURATION FILE ########\n#DO NOT MODIFY MANUALLY THIS FILE\n#VALUES WILL BE MODIFIED WHEN USING THE CONFIGURATION FORM\n'
DOMAIN_SERVER_CONFIGURATION_FILE_END = '########## END DOMAIN SERVER CONFIGURATION FILE'

#PROTOCOL_NAME_MAPPING_STATION_A = [('Prot1', 'buffer'), ('Prot2', 'beads'), ('Prot3', 'lysates')]
#PROTOCOL_NAME_MAPPING_STATION_B = [('Prot1', 'extraction')]
#PROTOCOL_NAME_MAPPING_STATION_C = [('Prot1', 'pcr')]

JSON_LABWARE_ROOT_FIELDS_TO_CHECK = ['metadata', 'dimensions','wells','parameters','brand']
JSON_LABWARE_FIELDS_TO_GET = {'brand':['brand'],'metadata':['displayName','displayCategory'],'dimensions':['xDimension',
        'yDimension', 'zDimension'],'parameters':['isMagneticModuleCompatible', 'loadName']}
JSON_LABWARE_WELL_TO_GET ={'wells':{'A1':['depth','totalLiquidVolume','shape', 'diameter','x','y','z']}}

INVALID_TEMPLATE_FILE = ['Invalid Protocol File ', 'Delimitation Parameters tags are not included in file']
INVALID_JSON_FILE = ['Invalid json File', 'File does not contains all requested information']

METADATA_FIELDS_FOR_PROTOCOL_TEMPLATE = ['protocolName', 'author', 'source','apiLevel']
PROTOCOL_STEPS_IN_TEMPLATE_FILE = ['prepare_mastermix', 'transfer_mastermix' , 'transfer_samples' ]
ADMIN_USERS = ['admin']

###### ERROR TEXT #############################################
ERROR_INVALID_FORMAT_FOR_DATES = ['Invalid date format. Use the format  (DD-MM-YYYY)']
ERROR_NOT_ROBOT_ACTION_MATCHES_FOUND = ['There is not robot actions that matches your query']
ERROR_INVALID_URL = ['Invalid domain server name']
ERROR_UNABLE_TO_SAVE_CONFIGURATION_FILE = ['Unable to save the configuration file']

####### URL for Rest Api ######################################
URL_FOR_REST_API_ROBOT_USAGE = '/api/robots/createUsage'
