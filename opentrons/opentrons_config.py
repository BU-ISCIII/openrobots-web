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
OPENTRONS_FIELD_TO_FETCH_IN_TEMPLATE_FILE = ['NUM_SAMPLES' , 'MM_LABWARE','MMTUBE_LABWARE', 'PCR_LABWARE', 'ELUTION_LABWARE',
            'PREPARE_MASTERMIX', 'TRANSFER_MASTERMIX', 'TRANSFER_SAMPLES', 'MM_TYPE']

LINE_FROM_PARAMETERS_START = '# Parameters to adapt the protocol'
LINE_FROM_PARAMETERS_END = '# End Parameters to adapt the protocol'
