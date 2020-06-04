import os, re, json
import sys, codecs
import datetime, time
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from openrobots.openrobots_config import *


def add_parameters_in_file (in_file, output_file, parameters, file_id):
    '''
    Description:
        The function will get protocol template file and add the parameters to create an output file
        that is stored in OPENROBOTS_OUTPUT_DIRECTORYthe Labware information used in the form to create the files
    Input:
        in_file     # template file
        output_file    # output file name
        parameters  # dictionnary with the information to include in the file
        file_id     # fileID
    Constans:
        OPENROBOTS_DELIMITATION_PARAMETERS_TAGS
        DOMAIN_SERVER
        URL_FOR_REST_API_ROBOT_USAGE
    Return:
        form_data
    '''
    template_dir = os.path.join(settings.MEDIA_ROOT, OPENROBOTS_TEMPLATE_DIRECTORY )
    template_file = os.path.join(template_dir, os.path.basename(in_file))
    if not os.path.exists(template_file):
        return 'Protocol Template does not exists'

    out_dir = os.path.join(settings.MEDIA_ROOT, OPENROBOTS_OUTPUT_DIRECTORY)
    out_file = os.path.join(out_dir, output_file )
    if not os.path.exists(out_dir) :
        os.makedirs (out_dir)

    with open (template_file, 'r') as in_fh:
        found_start = False
        delimitation_end_found = False
        parameters_added = True
        with open(out_file, 'w') as out_fh:
            for line in in_fh:
                parameter_section =  re.search(rf'^{OPENROBOTS_DELIMITATION_PARAMETERS_TAGS[0]}', line)
                end_parameter_section =  re.search(rf'^{OPENROBOTS_DELIMITATION_PARAMETERS_TAGS[1]}', line)
                if not found_start:
                    out_fh.write(line)
                if parameter_section :
                    found_start = True

                    for key in sorted(parameters):
                        type_of_data = get_type_of_data(parameters[key])
                        if type_of_data == 'boolean' or type_of_data == 'integer':

                            out_fh.write(key + ' = '+ parameters[key]+ '\n')
                        else:
                            out_fh.write(key + ' = \''+ parameters[key]+ '\'\n')
                    out_fh.write('PROTOCOL_ID = \'' + file_id + '\'\n')
                    out_fh.write('URL =  \'' + DOMAIN_SERVER + URL_FOR_REST_API_ROBOT_USAGE + '\'\n')
                    parameters_added = True
                    continue
                if end_parameter_section :
                    out_fh.write(line)
                    found_start = False
                    delimitation_end_found = True

    if parameters_added and delimitation_end_found :
        return 'True'
    os.remove(out_file)
    return 'Unable to write the parameters in the protocol file'

def get_type_of_data (data):
    '''
    Description:
        The function get always as input a string class.
        By trying to convert the input data to int or bolealn it will decide the type of data
        If not possible to conver it returns string
    Return:
        type_of_data
    '''
    boolean_values = ['True', 'False', 'None']
    if data in boolean_values :
        return 'boolean'
    try:
        integer = int(data)
        return 'integer'
    except:
        return 'string'




def get_metadata_from_file(in_file):
    '''
    Description:
        The function gets the metadata that are in the file
    Return:
        metadata
    '''
    metadata = {}
    with open (in_file, 'r') as in_fh:
        found_start = False
        for line in in_fh:
            metadata_section =  re.search(r'^metadata\s*=\s*{', line)
            if metadata_section:
                found_start = True
                continue
            end_metadata_section =  re.search(r'.*}', line)
            if found_start and end_metadata_section:
                break
            if found_start :
                line = line.rstrip()
                data = re.search(r'^\s*\'(.*)\'\s*:\s*\'(.*)\'', line)
                metadata[data.group(1)] = data.group(2)
                continue
    return metadata

def get_steps_used_in_protocol(in_file):
    '''
    Description:
        The function gets the the steps that are in protocol file
    Input:
        in_file     # input file name
    Constants:
        PROTOCOL_STEPS_IN_TEMPLATE_FILE
    Return:
        steps_in_file
    '''
    steps_in_file ={}
    # Initialice the steps to false
    for step in PROTOCOL_STEPS_IN_TEMPLATE_FILE :
        steps_in_file[step] = False

    with open (in_file, 'r') as fh:
        for line in fh :
            funtions_definition = re.search (r'^def\s+\w', line)
            if funtions_definition:
                for step in PROTOCOL_STEPS_IN_TEMPLATE_FILE :
                    if step in line:
                        steps_in_file[step] = True
                        break

    return steps_in_file



def json_file_valid_format(in_file):
    '''
    Description:
        The function check if file contains the lines included in OPENROBOTS_DELIMITATION_PARAMETERS_TAGS
    Input:
        in_file     # input file name
    Constants:
        OPENROBOTS_DELIMITATION_PARAMETERS_TAGS
    Return:
        True or False
    '''
    try:
        with open (in_file, 'r') as fh:
            json_dict = json.load(fh)
        for item in JSON_LABWARE_ROOT_FIELDS_TO_CHECK:
            if item not in json_dict:
                return False
    except:
        return False
    return True

def json_get_labware_information(in_file ):
    '''
    Description:
        The function fetch the labware information from json file
    Input:
        in_file     # input file name

    Constants:
        JSON_LABWARE_FIELDS_TO_GET
        JSON_LABWARE_WELL_TO_GET
    Return:
        json_data
    '''
    json_data = {}
    with open (in_file, 'r') as fh:
        json_dict = json.load(fh)
    for key in JSON_LABWARE_FIELDS_TO_GET.keys():
        for values in JSON_LABWARE_FIELDS_TO_GET[key]:
            json_data[values] = json_dict[key][values]
    for key in JSON_LABWARE_WELL_TO_GET.keys():
        for well in JSON_LABWARE_WELL_TO_GET[key].keys():
            for value in JSON_LABWARE_WELL_TO_GET[key][well] :
                json_data[value] = json_dict[key][well][value]

    json_data['colums'] = len(json_dict['ordering'])
    json_data['rows'] = len(json_dict['ordering'][0])
    json_data['num_wells'] = str(json_data['colums'] * json_data['rows'])
    json_data['spacing_col'] = "{:.2f}".format(float(json_dict['wells']['A2']['x']) - float(json_dict['wells']['A1']['x']))
    json_data['spacing_row'] = "{:.2f}".format(float(json_dict['wells']['A1']['y']) - float(json_dict['wells']['B1']['y']))

    return json_data


def store_user_file(in_file, store_folder):
    '''
    Description:
        The function gets the protocol template file. Add time stamp to the file name
        and stores on OPENROBOTS_TEMPLATE_DIRECTORY
    Input:
        in_file     # input file name
    Constants:

    Return:
        saved_file
    '''
    split_filename=re.search('(.*)(\.\w+$)',in_file.name)
    f_name = split_filename[1]
    f_extension = split_filename[2]
    fs_template = FileSystemStorage()
    timestr = time.strftime("%Y%m%d-%H%M%S")
    system_folder = os.path.join(settings.MEDIA_ROOT,store_folder)
    if not os.path.exists(system_folder):
        os.makedirs(system_folder)

    ## using the MEDIA_ROOT variable defined on settings to upload the file
    file_name=os.path.join(store_folder,  str(f_name + '_' +timestr + f_extension))
    filename = fs_template.save(file_name,  in_file)
    saved_file = os.path.join(settings.MEDIA_ROOT, file_name)
    return saved_file, file_name

def template_file_valid_format(in_file):
    '''
    Description:
        The function check if file contains the lines included in OPENROBOTS_DELIMITATION_PARAMETERS_TAGS
    Input:
        in_file     # input file name
    Constants:
        OPENROBOTS_DELIMITATION_PARAMETERS_TAGS
    Return:
        True or False
    '''

    with open (in_file, 'r') as fh:
        lines = fh.readlines()

    for tag in OPENROBOTS_DELIMITATION_PARAMETERS_TAGS:
        if not any(tag in s for s in lines) :
            return False
    return True
