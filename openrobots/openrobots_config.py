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

PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_A_PROT_1 = ['NUM_SAMPLES' , 'BUFFER_LABWARE','DESTINATION_LABWARE', 'DEST_TUBE', 'LANGUAGE','RESET_TIPCOUNT', 'VOLUME_BUFFER']
PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_A_PROT_2 = ['NUM_SAMPLES' , 'BEADS_LABWARE','PLATE_LABWARE','LANGUAGE', 'RESET_TIPCOUNT', 'DILUTE_BEADS', 'VOLUME_BEADS']
PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_A_PROT_3 = ['NUM_SAMPLES' , 'LYSATE_LABWARE','PLATE_LABWARE','LANGUAGE', 'RESET_TIPCOUNT', 'VOLUME_LYSATE', 'BEADS']

PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_B = ['NUM_SAMPLES', 'REAGENT_LABWARE','MAGPLATE_LABWARE', 'WASTE_LABWARE', 'ELUTION_LABWARE','LANGUAGE',
            'RESET_TIPCOUNT', 'DISPENSE_BEADS']

PROTOCOL_PARAMETERS_REQUIRED_FOR_STATION_C = ['NUM_SAMPLES' , 'MM_LABWARE','MMTUBE_LABWARE', 'PCR_LABWARE', 'ELUTION_LABWARE', 'LANGUAGE', 'VOLUME_ELUTION',
            'PREPARE_MASTERMIX', 'RESET_TIPCOUNT', 'TRANSFER_MASTERMIX', 'TRANSFER_SAMPLES', 'MM_TYPE']


MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_A_PROT_1 = [('NUM_SAMPLES','numberOfSamples') ,('BUFFER_LABWARE','bufferLabware'),('DESTINATION_LABWARE', 'destinationLabware'),
        ('DEST_TUBE', 'destinationTube'), ('LANGUAGE','languageCode'), ('RESET_TIPCOUNT', 'resetTipcount'),  ('VOLUME_BUFFER','volumeBuffer')]

MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_A_PROT_2 = [('NUM_SAMPLES','numberOfSamples') ,('BEADS_LABWARE','beadsLabware'),('PLATE_LABWARE', 'plateLabware'),
        ('LANGUAGE','languageCode'), ('RESET_TIPCOUNT', 'resetTipcount'), ('DILUTE_BEADS', 'diluteBeads'), ('VOLUME_BEADS', 'volumeBeads')]

MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_A_PROT_3 = [('NUM_SAMPLES','numberOfSamples') ,('LYSATE_LABWARE','lysateLabware'),('PLATE_LABWARE', 'plateLabware'),
        ('LANGUAGE','languageCode'), ('VOLUME_LYSATE', 'volumeLysate'),  ('RESET_TIPCOUNT', 'resetTipcount'), ('BEADS','beads')]

MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_B = [('NUM_SAMPLES','numberOfSamples') ,('REAGENT_LABWARE','reagentLabware'),('MAGPLATE_LABWARE', 'magPlateLabware'),
        ('WASTE_LABWARE', 'wasteLabware'), ('LANGUAGE','languageCode'), ('ELUTION_LABWARE','elutionLabware'),('DISPENSE_BEADS', 'dispenseBeads'),
        ('RESET_TIPCOUNT', 'resetTipcount') ]

MAP_PROTOCOL_PARAMETER_TO_DATABASE_STATION_C = [('NUM_SAMPLES','numberOfSamples') , ('MM_LABWARE','masterMixLabware'),('MMTUBE_LABWARE','masterMixTubeLabware'),
        ('PCR_LABWARE','pcrPlateLabware'), ('ELUTION_LABWARE','elutionLabware'), ('LANGUAGE','languageCode'), ('VOLUME_ELUTION', 'volumeElution'),
        ('PREPARE_MASTERMIX','prepareMastermix'),  ('RESET_TIPCOUNT', 'resetTipcount'), ('TRANSFER_MASTERMIX','transferMastermix'),
        ('TRANSFER_SAMPLES','transferSamples'), ('MM_TYPE','masterMixType')]
OPENROBOTS_DELIMITATION_PARAMETERS_TAGS = ['# Parameters to adapt the protocol',
                    '# End Parameters to adapt the protocol']


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
