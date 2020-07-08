from django.db import models
import time
from django.contrib.auth.models import User
from . import openrobots_config #OPENROBOTS_TEMPLATE_DIRECTORY, OPENROBOTS_OUTPUT_DIRECTORY
from distutils import util

## vale en la nueva version
class Stations (models.Model):
    stationName = models.CharField(max_length = 80)
    description = models.CharField(max_length = 255, null = True, blank = True )

    def __str__ (self):
        return '%s' %(self.stationName)

    def get_station_name(self):
        return '%s' %(self.stationName)

## vale en la nueva version
class ModuleType (models.Model):
    moduleType = models.CharField(max_length = 30)
    vendor = models.CharField(max_length = 30)
    description = models.CharField(max_length = 255, null = True, blank = True)
    witePapers = models.FileField(upload_to = openrobots_config.OPENROBOTS_MODULE_TYPE_GUIDES_DIRECTORY , null = True , blank = True)
    manualGuide = models.FileField(upload_to = openrobots_config.OPENROBOTS_MODULE_TYPE_GUIDES_DIRECTORY , null = True , blank = True)
    moduleImage = models.FileField(upload_to = openrobots_config.OPENROBOTS_MODULE_TYPE_GUIDES_DIRECTORY , null = True , blank = True)

    def __str__ (self):
        return '%s' %(self.moduleType)

    def get_module_type_name(self):
        return '%s' %(self.moduleType)

    def get_module_vendor(self):
        return '%s' %(self.vendor)

    def get_minimum_module_data(self):
        data = []
        data.append(self.moduleType)
        data.append(self.vendor)
        data.append(self.pk)
        return data

    def get_main_module_data(self):
        data = []
        data.append(self.moduleType)
        data.append(self.vendor)
        data.append(self.description)
        return data

    def get_image(self):
        return '%s' %(self.moduleImage)

    def get_documents (self):
        data = []
        data.append(self.witePapers)
        data.append(self.manualGuide)
        return data
## vale en la nueva version
class ModulesInLab (models.Model):
    moduleType = models.ForeignKey(
                        ModuleType,
                        on_delete=models.CASCADE)
    moduleID = models.CharField(max_length = 30)
    description = models.CharField(max_length =255, null = True, blank = True)

    def __str__ (self):
        return '%s_%s' %(self.moduleType ,self.moduleID)

    def get_module_type (self):
        return '%s' %(self.moduleType.get_module_type_name())

    def get_module_type_and_ID (self):
        return '%s_%s' %(self.moduleType ,self.moduleID)

    def get_moduleID (self):
        return '%s' %(self.moduleID)

    def get_module_id (self):
        return '%s' %(self.pk)

class RobotsInventoryManager (models.Manager):

    def create_robot(self, robot_data):
        configuration_obj = Stations.objects.get(stationName__exact = robot_data['configuration'])
        new_robot = self.create( userName = robot_data['userName'], configuration = configuration_obj, location = robot_data['location'],
                robots = robot_data['robots'], serialNumber= robot_data['serialNumber'],
                IP_address = robot_data['IP_address'], hostName= robot_data['hostName'],
                computer_mac = robot_data['computer_mac'], rightPipette= robot_data['rightPipette'], leftPipette = robot_data['leftPipette'],
                rightPipetteID = robot_data['rightPipetteID'], leftPipetteID = robot_data['leftPipetteID'],
                neededPlugs = robot_data['neededPlugs'], observations = robot_data['observations'] )
        return new_robot


## vale en la nueva version
class RobotsInventory (models.Model):
    userName = models.ForeignKey (
                        User,
                        on_delete=models.CASCADE, null = True, blank = True )
    configuration = models.ForeignKey(
                        Stations,
                        on_delete=models.CASCADE)
    modules = models.ManyToManyField(ModulesInLab, blank = True)
    location = models.CharField(max_length = 255)
    robots = models.CharField(max_length = 255)
    serialNumber = models.CharField(max_length = 255)
    IP_address = models.CharField(max_length = 50)
    hostName = models.CharField(max_length = 50)
    computer_mac = models.CharField(max_length = 50)
    rightPipette = models.CharField(max_length = 20, null = True, blank = True)
    leftPipette = models.CharField(max_length = 20, null = True, blank = True)
    rightPipetteID = models.CharField(max_length = 20, null = True, blank = True)
    leftPipetteID = models.CharField(max_length = 255, null = True, blank = True)
    neededPlugs  = models.CharField(max_length = 255, null = True, blank = True)
    observations = models.CharField(max_length = 255, null = True, blank = True)
    generatedat = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return '%s' %(self.robots)

    def get_robot_name (self):
        return '%s' %(self.robots)

    def get_robot_id (self):
        return '%s'  %(self.pk)

    def get_station_name(self):
        return '%s' %(self.configuration.get_station_name())

    def get_minimum_robot_data(self):
        data = []
        data.append(self.robots)
        data.append(self.location)
        data.append(self.configuration.get_station_name())
        data.append(self.pk)
        return data

    def get_basic_robot_data(self):
        data = []
        data.append(self.robots)
        data.append(self.location)
        data.append(self.configuration.get_station_name())
        data.append(self.serialNumber)
        data.append(self.observations)
        return data

    def get_network_data(self):
        data = []
        data.append(self.IP_address)
        data.append(self.hostName)
        data.append(self.computer_mac)
        return data

    def get_pipette_data(self):
        data = []
        data.append(self.rightPipette)
        data.append(self.rightPipetteID)
        data.append(self.leftPipette)
        data.append(self.leftPipetteID)
        return data

    def get_modules_obj(self):

        return self.modules

    def get_plugs_data(self):
        data = []
        data.append(self.neededPlugs)
        return data

    def set_module(self, module_obj) :
        self.modules.add(module_obj)
        self.save()
        return

    objects = RobotsInventoryManager()

## vale en la nueva version
class ProtocolsType (models.Model):
    protocolTypeName = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255, null = True, blank = True )

    def __str__ (self):
        return '%s' %(self.protocolTypeName)

    def get_name(self):
        return '%s' %(self.protocolTypeName)

class ProtocolTemplateFilesManager(models.Manager) :
    def create_protocol_template (self, protocol_data):
        protocol_obj = ProtocolsType.objects.get(protocolTypeName__exact = protocol_data['typeOfProtocol'])
        station_obj = Stations.objects.get(stationName__exact = protocol_data['station'])
        new_protocol_template = self.create(userName = protocol_data ['user'],station = station_obj,  typeOfProtocol = protocol_obj,
                    protocolTemplateFileName = protocol_data['file_name'], protocolName = protocol_data['protocolName'],
                    authors= protocol_data['author'], source = protocol_data['source'], apiLevel= protocol_data['apiLevel'],
                    protocolNameInForm = protocol_data['prottype'] , protocolNumber = protocol_data['protocolNumber'],
                    protocolVersion = protocol_data['protocolVersion'])
        return new_protocol_template
## vale en la nueva version
class ProtocolTemplateFiles (models.Model):
    userName = models.ForeignKey (
                        User,
                        on_delete=models.CASCADE, null = True, blank = True )
    station = models.ForeignKey(
                        Stations,
                        on_delete=models.CASCADE)
    typeOfProtocol = models.ForeignKey(
                        ProtocolsType,
                        on_delete=models.CASCADE)
    protocolNameInForm = models.CharField(max_length = 80, null = True)
    protocolTemplateFileName = models.FileField(upload_to = openrobots_config.OPENROBOTS_TEMPLATE_DIRECTORY )
    protocolName = models.CharField(max_length = 255)
    protocolNumber =  models.CharField(max_length = 10, null = True, blank = True)
    protocolVersion =  models.CharField(max_length = 10, null = True, blank = True)
    authors = models.CharField(max_length = 255)
    source = models.CharField(max_length = 255)
    apiLevel = models.CharField(max_length = 50)
    #prepareMasterMix = models.BooleanField(default = False)
    #transferMasterMix = models.BooleanField(default = False)
    #transferSamples = models.BooleanField(default = False)
    parametersDefined = models.BooleanField(default = False, null = True)
    protocolTemplateBeUsed = models.BooleanField(default = False, null = True)
    generatedat = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return '%s' %(self.protocolNameInForm)

    def get_protocol_file_name(self):
        return '%s' %(self.protocolTemplateFileName)

    def get_protocol_name(self):
        return '%s' %(self.protocolName)

    def get_protocol_number(self):
        return '%s'  %(self.protocolNumber)

    def get_protocol_version(self):
        return '%s' %(self.protocolVersion)

    def get_protocol_file(self):
        return '%s' %(self.protocolTemplateFileName)

    def get_protocol_type(self):
        return '%s' %(self.typeOfProtocol.get_name())

    def get_station(self):
        return '%s' %(self.station.get_station_name())

    def get_main_data(self):
        data = []
        data.append(self.id)
        data.append(self.typeOfProtocol.get_name())
        data.append(self.station.get_station_name())
        data.append(self.userName)
        data.append(self.protocolName)
        data.append(self.protocolTemplateFileName)
        return data

    def get_metadata(self):
        data = []
        data.append(self.protocolName)
        data.append(self.authors)
        data.append(self.source)
        data.append(self.apiLevel)
        return data
    def get_name_in_form(self):
        return '%s' %(self.protocolNameInForm)

    def get_protocol_template_id (self):
        return '%s'  %(self.pk)

    def set_parameters_defined (self):
        self.parametersDefined = True
        self.save()
        return self

    def set_template_do_not_use(self):
        self.protocolTemplateBeUsed = False
        self.save()
        return self

    def set_template_to_be_used(self):
        self.protocolTemplateBeUsed = True
        self.save()
        return self

    objects = ProtocolTemplateFilesManager()

class ElutionHardware (models.Model):
    hardwareType = models.CharField(max_length = 80)

    def __str__ (self):
        return '%s' %(self.hardwareType)

    def get_hardware_type(self):
        return '%s' %(self.hardwareType)


class InventoryLabwareManager(models.Manager):
    def create_inventory_labware(self,data):

        new_inventory_labware = self.create( elution_LabwareType = data['displayName'],
                valueInCode = data['loadName'], brand = data['brand'], category= data['displayCategory'],
                x_dimension = data['xDimension'], y_dimension = data['yDimension'], z_dimension = data['zDimension'],
                num_columns= data['colums'],  num_rows = data['rows'], spacing_col = data['spacing_col'],
                spacing_row = data['spacing_row'], well_depth = data['depth'], well_shape = data['shape'],
                well_volume = data['totalLiquidVolume'], well_diameter = data['diameter'], num_wells = data['num_wells'],
                jsonFile= data['jsonFile'], pythonFile = data['pythonFile'], imageFile = data['imageFile'] )

        return new_inventory_labware

class InventoryLabware (models.Model):
    elution_LabwareType = models.CharField(max_length = 80)
    valueInCode = models.CharField(max_length = 255)
    brand = models.CharField(max_length = 80)
    category = models.CharField(max_length = 80)
    x_dimension = models.CharField(max_length = 10)
    y_dimension = models.CharField(max_length = 10)
    z_dimension = models.CharField(max_length = 10)
    num_columns = models.CharField(max_length = 5)
    num_rows = models.CharField(max_length = 5)
    num_wells = models.CharField(max_length = 5)
    spacing_col = models.CharField(max_length = 10)
    spacing_row = models.CharField(max_length = 10)
    well_depth = models.CharField(max_length = 5)
    well_shape = models.CharField(max_length = 20)
    well_volume = models.CharField(max_length = 10)
    well_diameter = models.CharField(max_length = 10)
    jsonFile = models.FileField(upload_to = openrobots_config.OPENROBOTS_LABWARE_JSON_DIRECTORY , null = True, blank = True, max_length=200)
    pythonFile = models.FileField(upload_to = openrobots_config.OPENROBOTS_LABWARE_PYTHON_DIRECTORY, null = True, blank = True ,max_length=200 )
    imageFile = models.FileField(upload_to = openrobots_config.OPENROBOTS_LABWARE_IMAGE_DIRECTORY, null = True, blank = True ,max_length=200)
    generatedat = models.DateTimeField(auto_now_add=True)


    def __str__ (self):
        return '%s' %(self.elution_LabwareType)

    def get_elution_labware_type (self):
        return '%s' %(self.elution_LabwareType)

    def get_minimun_elution_lab_data (self):
        data = []
        data.append(self.elution_LabwareType)
        data.append(self.brand)
        data.append(self.category)
        data.append(self.num_wells)
        data.append(self.pk)
        return data

    def get_basic_labware_data(self):
        data = []
        #data.append(self.elutionHW_type.get_hardware_type())
        data.append(self.brand)
        data.append(self.category)
        return data

    def get_image(self):
        return '%s' %(self.imageFile)

    def get_files(self):
        data = []
        data.append(self.jsonFile)
        data.append(self.pythonFile)
        return data

    def get_plate_data(self):
        data = []
        data.append(self.num_columns)
        data.append(self.num_rows)
        data.append(self.num_columns)
        data.append(self.x_dimension)
        data.append(self.y_dimension)
        data.append(self.z_dimension)
        return data

    def get_well_data(self):
        data = []
        data.append(self.well_volume)
        data.append(self.well_shape)
        data.append(self.well_diameter)
        data.append(self.well_depth)
        data.append(self.spacing_row)
        data.append(self.spacing_col)
        return data

    objects = InventoryLabwareManager()


class ProtocolParameterManager(models.Manager):
    def create_parameter(self, parameter_data,template_file_id):
        usedTemplateFile = ProtocolTemplateFiles.objects.get(pk__exact = template_file_id)
        new_parameter = self.create(usedTemplateFile = usedTemplateFile, parameterType = parameter_data['parameterType'],
                        parameterName = parameter_data['parameterName'], nameInForm = parameter_data['nameInForm'],
                        defaultValue = parameter_data['defaultValue'])
        return new_parameter


class ProtocolParameter (models.Model):
    usedTemplateFile = models.ForeignKey(
                        ProtocolTemplateFiles,
                        on_delete=models.CASCADE)
    parameterType = models.CharField(max_length = 20)
    parameterName = models.CharField(max_length = 50)
    nameInForm = models.CharField(max_length = 50)
    defaultValue = models.CharField(max_length = 50, null = True, blank = True)

    def __str__ (self):
        return '%s__%s' %(self.usedTemplateFile, self.parameterName)

    def get_parameter_name (self):
        return '%s' %(self.parameterName)

    def get_default_value(self):
        return '%s' %(self.defaultValue)
    def get_parameter_info(self):
        data = []
        data.append(self.parameterName)
        data.append(self.nameInForm)
        data.append(self.defaultValue)
        return data

    def get_parameter_type(self):
        return '%s' %(self.parameterType)

    objects = ProtocolParameterManager()


class ParameterOptionManager(models.Manager):
    def create_parameter_option(self, option_data):
        if option_data['optionDescription'] == '':
            optionDescription = None
        else:
            optionDescription = option_data['optionDescription']
        new_parameter_option = self.create( parameter = option_data['parameter'],
                    optionValue = option_data['optionValue'],  default = option_data['default'],
                    optionDescription = optionDescription )


class ParameterOption (models.Model):
    parameter = models.ForeignKey(
                        ProtocolParameter,
                        on_delete=models.CASCADE)
    optionValue = models.CharField(max_length = 80)
    optionDescription = models.CharField(max_length = 80, null = True)
    default = models.CharField(max_length = 5, null = True, blank = True)

    def __str__ (self):
        return '%s' %(self.optionValue)

    def get_option_value (self):
        return '%s' %(self.optionValue)

    def get_option_description(self):
        if self.optionDescription == None:
            description = ''
        else:
            description = self.optionDescription
        return  description

    objects = ParameterOptionManager()


class ProtocolRequestManager(models.Manager):
    def create_protocol_request(self,request_data):
        protocolTemplate = ProtocolTemplateFiles.objects.get(pk__exact = request_data['template_id'])
        new_protocol_request = self.create( protocolTemplate = protocolTemplate,
                            userRequestedBy = request_data['user'], requestedCodeID = request_data['requestedCodeID'],
                            generatedFile = request_data['generatedFile'], protocolID = request_data['protocolID'],
                            stationName = request_data['station'], templateProtocolNumber = request_data['templateProtocolNumber'],
                            userNotes = request_data['usernotes'])
        return new_protocol_request


class ProtocolRequest(models.Model):
    protocolTemplate = models.ForeignKey(
                        ProtocolTemplateFiles,
                        on_delete=models.CASCADE)
    userRequestedBy = models.ForeignKey (
                        User,
                        on_delete=models.CASCADE, null = True, blank = True )
    requestedCodeID = models.CharField(max_length = 50)
    protocolID = models.CharField(max_length = 50)
    generatedFile = models.FileField(upload_to = openrobots_config.OPENROBOTS_OUTPUT_DIRECTORY )
    stationName = models.CharField(max_length = 25)
    templateProtocolNumber = models.CharField(max_length = 10)

    userNotes = models.CharField(max_length = 255)
    generatedat = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return '%s' %(self.requestedCodeID)

    def get_result_data(self):
        data = []
        data.append(self.requestedCodeID)
        data.append(self.protocolTemplate.get_protocol_type())
        data.append(self.generatedFile)
        return data

    def get_user_requested(self):
        return '%s' %(self.userRequestedBy.username)

    def get_request_info(self):
        data = []
        data.append(self.userRequestedBy.username)
        data.append(self.requestedCodeID)
        data.append(self.generatedat.strftime("%Y-%b-%d"))
        data.append(self.generatedFile)
        return data

    objects = ProtocolRequestManager()

class ProtocolParameterValuesManager(models.Manager):
    def create_parameter_value (self, param_value):
        new_parameter_value = self.create(protocolRequest = param_value['protocolRequest'],
                        parameterName = param_value['parameterName'],  parameterValue = param_value['parameterValue'])
        return new_parameter_value

class ProtocolParameterValues(models.Model):
    protocolRequest = models.ForeignKey(
                        ProtocolRequest,
                        on_delete=models.CASCADE)
    parameterName = models.CharField(max_length = 60)
    parameterValue = models.CharField(max_length = 60)

    def __str__ (self):
        return '%s' %(self.protocolRequest)

    def get_name_and_value(self):
        return (self.parameterName, self.parameterValue)

    objects = ProtocolParameterValuesManager()



class FileIDUserRequestMappingManager(models.Manager):

    def create_file_id_user (self, request_data):
        new_file_id = self.create( fileID= request_data['fileID'], station= request_data['station'],
                                protocol = request_data['protocol'])
        return new_file_id


class FileIDUserRequestMapping(models.Model):
    fileID = models.CharField(max_length = 50)
    station = models.CharField(max_length = 20)
    protocol = models.CharField(max_length = 50)
    generatedat = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return '%s' %(self.fileID)

    def get_file_id (self):
        return '%s' %(self.fileID)

    def get_station_protocol(self):
        return '%s' %(self.protocol)

    def get_station(self):
        return '%s' %(self.station)



    objects = FileIDUserRequestMappingManager()



class RobotsActionPost(models.Model):
    ownerProtocol = models.ForeignKey (
                        User,
                        on_delete=models.CASCADE, null = True, blank = True )
    ipaddress = models.CharField(max_length = 50,  null = True)
    stationType = models.CharField(max_length = 50,  null = True, blank = True)
    RobotID = models.CharField(max_length = 50)
    executedAction = models.CharField(max_length = 250)
    ProtocolID = models.CharField(max_length = 50, null = True)
    StartRunTime =models.DateTimeField(max_length = 50,  null = True)
    FinishRunTime = models.DateTimeField(max_length = 50,  null = True)
    modifiedParameters = models.BooleanField(default = False)
    generatedat = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return '%s' %(self.RobotID)

    def get_executed_action(self):
        return '%s' %(self.executedAction)

    def get_station_type(self):
        return '%s' %(self.stationType)

    def get_robot_name (self):
        return '%s' %(self.RobotID)

    def get_protocol_id(self):
        return '%s' %(self.ProtocolID)



    def get_robot_action_data (self):
        data=[]
        try:
            data.append(self.ownerProtocol.username)
        except:
            data.append('Not recorded')
        data.append(self.executedAction)
        data.append(self.StartRunTime.strftime("%Y-%b-%d  %H:%M"))
        data.append(self.FinishRunTime.strftime("%Y-%b-%d %H:%M"))
        data.append(str(self.FinishRunTime - self.StartRunTime))
        data.append(str(self.modifiedParameters))
        data.append(str(self.pk))
        return data

    def update_modified_parameters(self, value):
        self.modifiedParameters = value
        self.save()
        return self

    def update_protocol_owner(self, user):
        self.ownerProtocol = user
        self.save()
        return self

    def update_robot_station_type(self, station_robot):
        self.stationType = station_robot
        self.save()
        return self

class ParametersRobotActionManager(models.Manager):
    def create_parameter(self, request_data):
        new_parameter = self.create( robotActionPost = request_data['robotActionPost'],  ProtocolRequest= request_data['ProtocolRequest'],
                    parameterName = request_data['parameterName'], parameterValue = request_data['parameterValue'],
                    protocolID = request_data['protocolID'],  modified = request_data['modified'])

        return new_parameter


class ParametersRobotAction (models.Model):
    robotActionPost = models.ForeignKey (
                        RobotsActionPost,
                        on_delete=models.CASCADE )
    ProtocolRequest = models.ForeignKey (
                        ProtocolRequest,
                        on_delete=models.CASCADE, null = True, blank = True )
    protocolFileID = models.ForeignKey (
                        FileIDUserRequestMapping,
                        on_delete=models.CASCADE , null = True)
    protocolID = models.CharField(max_length = 20, null = True)
    parameterName = models.CharField(max_length = 80)
    parameterValue = models.CharField(max_length = 80)
    modified = models.BooleanField(default = False)
    generatedat = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return '%s_%s' %(self.robotActionPost, self.protocolFileID)

    def get_parameter_name_and_value(self):
        return (self.parameterName, self.parameterValue )

    def get_modified_field(self):
        return self.modified

    objects = ParametersRobotActionManager()
