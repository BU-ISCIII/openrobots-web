import os
from django.conf import settings
##### Allow to import the configuration samba files from configuration folder
import sys
sys.path.append('../')


############## FOLDER SETTINGS ###############################
## Directory settings for processing the run data files ######
## Relative path from settings.BASE_DIR

## Relative path from settings.MEDIA_ROOT
OPENTRONS_TEMPLATE_DIRECTORY = 'template'
OPENTRONS_OUTPUT_DIRECTORY = 'ouput_files'


OPENTRONS_TEMPLATE_FILE_NAME = 'v1_station_c_S3.ot2.apiv2.py'
OPENTRONS_FIELD_TO_FETCH_IN_TEMPLATE_FILE_STATION_3 = ['NUM_SAMPLES' , 'MM_LABWARE','MMTUBE_LABWARE', 'PCR_LABWARE', 'ELUTION_LABWARE',
            'PREPARE_MASTERMIX', 'TRANSFER_MASTERMIX', 'TRANSFER_SAMPLES', 'MM_TYPE']

OPENTRONS_DELIMITATION_PARAMETERS_TAGS = ['# Parameters to adapt the protocol',
                    '# End Parameters to adapt the protocol']

INVALID_TEMPLATE_FILE = ['Invalid Protocol File ', 'Delimitation Parameters tags are not included in file']
METADATA_FIELDS_FOR_PROTOCOL_TEMPLATE = ['protocolName', 'author', 'source','apiLevel']
PROTOCOL_STEPS_IN_TEMPLATE_FILE = ['prepare_mastermix', 'transfer_mastermix' , 'transfer_samples' ]
ADMIN_USERS = ['admin']
