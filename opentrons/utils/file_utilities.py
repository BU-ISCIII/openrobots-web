import os, re
from django.conf import settings
from opentrons.opentrons_config import *

def add_parameters_in_file ( parameters):

    template_dir = os.path.join(settings.MEDIA_ROOT, OPENTRONS_TEMPLATE_DIRECTORY )
    template_file = os.path.join(template_dir, OPENTRONS_TEMPLATE_FILE_NAME)
    if not os.path.exists(template_file):
        return

    out_dir = os.path.join(settings.MEDIA_ROOT, OPENTRONS_OUTPUT_DIRECTORY)
    out_file = os.path.join(out_dir,'pepe.py')
    if not os.path.exists(out_dir) :
        os.makedirs (out_dir)
    with open (template_file, 'r') as in_fh:
        found_start = False
        with open(out_file, 'w') as out_fh:
            for line in in_fh:
                parameter_section =  re.search(rf'^{LINE_FROM_PARAMETERS_START}', line)
                end_parameter_section =  re.search(rf'^{LINE_FROM_PARAMETERS_END}', line)
                if not found_start:
                    out_fh.write(line)
                if parameter_section :
                    found_start = True
                    for param in OPENTRONS_FIELD_TO_FETCH_IN_TEMPLATE_FILE :

                        out_fh.write(param + ' = '+ parameters[param]+ '\n')
                    continue
                if end_parameter_section :
                    break
                    #out_fh.write(line)
                    #found_start = False
    return out_file
