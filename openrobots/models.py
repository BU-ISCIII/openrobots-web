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

class MasterMixType (models.Model):
    MasterMixType = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255, null = True, blank = True )
    default = models.BooleanField(default=None)

    def __str__ (self):
        return '%s' %(self.MasterMixType)

    def get_master_mix_type (self):
        return '%s' %(self.MasterMixType)

class MasterMixLabware (models.Model):
    MasterMixLabwareType = models.CharField(max_length = 80)
    description = models.CharField(max_length = 255)
    default = models.BooleanField(default=None)

    def __str__ (self):
        return '%s' %(self.MasterMixLabwareType)

    def get_mastermix_labware_type (self):
        return '%s' %(self.MasterMixLabwareType)

class MasterMixTube (models.Model):
    MasterMixTube = models.CharField(max_length = 80)
    MasterMixRadius = models.CharField(max_length = 80)
    default = models.BooleanField(default=None)

    def __str__ (self):
        return '%s' %(self.MasterMixTube)
    def get_mastermix_tube (self):
        return '%s' %(self.MasterMixTube)

class PCR_plateLabware (models.Model):
    PCR_plateLabwareType = models.CharField(max_length = 80)
    description = models.CharField(max_length = 255)
    default = models.BooleanField(default=None)

    def __str__ (self):
        return '%s' %(self.PCR_plateLabwareType)

    def get_pcr_plate_labware_type (self):
        return '%s' %(self.PCR_plateLabwareType)


class MagPlate_Labware(models.Model):
    mag_plateLabwareType = models.CharField(max_length = 80)
    description = models.CharField(max_length = 255)
    default = models.BooleanField(default=None)

    def __str__ (self):
        return '%s' %(self.mag_plateLabwareType)
    def get_mag_plate_name (self):
        return '%s' %(self.mag_plateLabwareType)


class Buffer_Labware(models.Model):
    bufferLabwareType = models.CharField(max_length = 80)
    description = models.CharField(max_length = 255)
    default = models.BooleanField(default=None)

    def __str__ (self):
        return '%s' %(self.bufferLabwareType)
    def get_buffer_name (self):
        return '%s' %(self.bufferLabwareType)


class Destination_Labware(models.Model):
    destinationLabwareType = models.CharField(max_length = 80)
    description = models.CharField(max_length = 255)
    default = models.BooleanField(default=None)

    def __str__ (self):
        return '%s' %(self.destinationLabwareType)
    def get_destination_labware_name (self):
        return '%s' %(self.destinationLabwareType)


class Destination_Tube_Labware(models.Model):
    destinationTube = models.CharField(max_length = 80)
    description = models.CharField(max_length = 255)
    default = models.BooleanField(default=None)

    def __str__ (self):
        return '%s' %(self.destinationTube)
    def get_destination_tube_name (self):
        return '%s' %(self.destinationTube)

class Beads_Labware(models.Model):
    beadsLabwareType = models.CharField(max_length = 80)
    description = models.CharField(max_length = 255)
    default = models.BooleanField(default=None)

    def __str__ (self):
        return '%s' %(self.beadsLabwareType)
    def get_beads_labware_name (self):
        return '%s' %(self.beadsLabwareType)

class Plate_Labware(models.Model):
    plateLabwareType = models.CharField(max_length = 80)
    description = models.CharField(max_length = 255)
    default = models.BooleanField(default=None)

    def __str__ (self):
        return '%s' %(self.plateLabwareType)
    def get_plate_labware_name (self):
        return '%s' %(self.plateLabwareType)

class Lysate_Labware(models.Model):
    lysateLabwareType = models.CharField(max_length = 80)
    description = models.CharField(max_length = 255)
    default = models.BooleanField(default=None)

    def __str__ (self):
        return '%s' %(self.lysateLabwareType)
    def get_lysate_labware_name (self):
        return '%s' %(self.lysateLabwareType)

class Lysate_Tube (models.Model):
    lysateTube = models.CharField(max_length = 80)
    description = models.CharField(max_length = 255)
    default = models.BooleanField(default=None)

    def __str__ (self):
        return '%s' %(self.lysateTube)
    def get_lysate_tube (self):
        return '%s' %(self.lysateTube)

class ElutionStationB_Labware(models.Model):
    elutionStationB = models.CharField(max_length = 80)
    description = models.CharField(max_length = 255)
    default = models.BooleanField(default=None)

    def __str__ (self):
        return '%s' %(self.elutionStationB)
    def get_elution_station_b (self):
        return '%s' %(self.elutionStationB)

class ElutionStationC_Labware(models.Model):
    elutionStationC = models.CharField(max_length = 80)
    description = models.CharField(max_length = 255)
    default = models.BooleanField(default=None)

    def __str__ (self):
        return '%s' %(self.elutionStationC)
    def get_elution_station_c (self):
        return '%s' %(self.elutionStationC)

class Tips300_Labware(models.Model):
    tips300 = models.CharField(max_length = 80)
    description = models.CharField(max_length = 255)
    default = models.BooleanField(default=None)

    def __str__ (self):
        return '%s' %(self.tips300)
    def get_tips300_labware (self):
        return '%s' %(self.tips300)

class Tips1000_Labware(models.Model):
    tips1000 = models.CharField(max_length = 80)
    description = models.CharField(max_length = 255)
    default = models.BooleanField(default=None)

    def __str__ (self):
        return '%s' %(self.tips1000)
    def get_tips1000_labware (self):
        return '%s' %(self.tips1000)

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
    #elutionHW_type =  models.ForeignKey (
    #                   ElutionHardware,
    #                    on_delete=models.CASCADE, max_length = 80, null = True, blank = True )
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



class Reagent_Labware(models.Model):
    reagentLabwareType = models.CharField(max_length = 80)
    description = models.CharField(max_length = 255)
    default = models.BooleanField(default=None)

    def __str__ (self):
        return '%s' %(self.reagentLabwareType)
    def get_reagent_labware_name (self):
        return '%s' %(self.reagentLabwareType)

class Waste_Labware(models.Model):
    wasteLabwareType = models.CharField(max_length = 80)
    description = models.CharField(max_length = 255)
    default = models.BooleanField(default=None)

    def __str__ (self):
        return '%s' %(self.wasteLabwareType)

    def get_waste_labware_name (self):
        return '%s' %(self.wasteLabwareType)


class Language(models.Model):
    languageCode = models.CharField(max_length = 10)
    languageDescription = models.CharField(max_length = 80)
    default = models.BooleanField(default=None)

    def __str__ (self):
        return '%s' %(self.languageCode)

    def get_language_code (self):
        return '%s' %(self.languageCode)

class RequestForStationA_Prot1Manager(models.Manager):

    def create_new_request (self, request_data):
        bufferLabware =  Buffer_Labware.objects.get(bufferLabwareType__exact = request_data['bufferLabware'])
        destinationLabware =  Destination_Labware.objects.get(destinationLabwareType__exact = request_data['destinationLabware'])
        destinationTube =  Destination_Tube_Labware.objects.get(destinationTube__exact = request_data['destinationTube'])
        usedTemplateFile = ProtocolTemplateFiles.objects.get(protocolTemplateFileName__exact = request_data['usedTemplateFile'])
        languageCode = Language.objects.filter(languageCode__exact = request_data['languageCode']).last()
        tips1000 = Tips1000_Labware.objects.filter(tips1000 = request_data['tips1000']).last()
        new_request = self.create(userRequestedBy = request_data['userRequestedBy'], bufferLabware = bufferLabware,
                    destinationLabware = destinationLabware, destinationTube = destinationTube, languageCode = languageCode,
                    usedTemplateFile = usedTemplateFile, requestedCodeID = request_data['requestedCodeID'],
                    numberOfSamples = request_data['numberOfSamples'],  protocolID = request_data['protocolID'],
                    volumeBuffer = request_data['volumeBuffer'], generatedFile = request_data['generatedFile'] ,
                    resetTipcount = util.strtobool(request_data['resetTipcount']), userNotes = request_data['userNotes'],
                    tips1000 = tips1000)

        return new_request

class RequestForStationA_Prot1 (models.Model):
    userRequestedBy = models.ForeignKey (
                        User,
                        on_delete=models.CASCADE, null = True, blank = True )
    bufferLabware = models.ForeignKey (
                        Buffer_Labware,
                        on_delete=models.CASCADE, null = True, blank = True )

    destinationLabware = models.ForeignKey (
                        Destination_Labware,
                        on_delete=models.CASCADE, null = True, blank = True )
    destinationTube = models.ForeignKey (
                        Destination_Tube_Labware,
                        on_delete=models.CASCADE, null = True, blank = True )

    usedTemplateFile = models.ForeignKey(
                        ProtocolTemplateFiles,
                        on_delete=models.CASCADE)
    languageCode = models.ForeignKey(
                        Language,
                        on_delete=models.CASCADE, null = True)
    tips1000 = models.ForeignKey(
                        Tips1000_Labware,
                        on_delete=models.CASCADE, null = True)
    requestedCodeID = models.CharField(max_length = 50)
    protocolID = models.CharField(max_length = 50, default = None)
    numberOfSamples = models.CharField(max_length = 10)
    volumeBuffer = models.CharField(max_length = 10)
    resetTipcount = models.BooleanField(default=None)
    generatedFile = models.FileField(upload_to = openrobots_config.OPENROBOTS_OUTPUT_DIRECTORY )
    userNotes = models.CharField(max_length = 255)
    generatedat = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return '%s' %(self.requestedCodeID)

    def get_result_data(self):
        data = []
        data.append(self.requestedCodeID)
        data.append(self.usedTemplateFile.get_protocol_type())
        data.append(self.generatedFile)
        return data

    def get_request_info(self):
        data = []
        data.append(self.userRequestedBy.username)
        data.append(self.requestedCodeID)
        data.append(self.generatedat.strftime("%Y-%b-%d"))
        data.append(self.generatedFile)
        return data

    def get_user_file(self):
        return '%s' %(self.userRequestedBy.username)

    def get_user_file_obj(self):
        return self.userRequestedBy

    objects = RequestForStationA_Prot1Manager()


class RequestForStationA_Prot2Manager(models.Manager):

    def create_new_request (self, request_data):
        beadsLabware =  Beads_Labware.objects.get(beadsLabwareType__exact = request_data['beadsLabware'])
        plateLabware =  Plate_Labware.objects.get(plateLabwareType__exact = request_data['plateLabware'])
        usedTemplateFile = ProtocolTemplateFiles.objects.get(protocolTemplateFileName__exact = request_data['usedTemplateFile'])
        languageCode = Language.objects.filter(languageCode__exact = request_data['languageCode']).last()
        tips1000 = Tips1000_Labware.objects.filter(tips1000 = request_data['tips1000']).last()
        new_request = self.create(userRequestedBy = request_data['userRequestedBy'], beadsLabware = beadsLabware,
                    plateLabware = plateLabware, usedTemplateFile = usedTemplateFile, languageCode = languageCode,
                    requestedCodeID = request_data['requestedCodeID'], numberOfSamples = request_data['numberOfSamples'],
                    volumeBeads = request_data['volumeBeads'],  protocolID = request_data['protocolID'],
                    resetTipcount = util.strtobool(request_data['resetTipcount']), diluteBeads = util.strtobool(request_data['diluteBeads']),
                    generatedFile = request_data['generatedFile'] , userNotes = request_data['userNotes'],
                    tips1000 = tips1000)

        return new_request

class RequestForStationA_Prot2 (models.Model):
    userRequestedBy = models.ForeignKey (
                        User,
                        on_delete=models.CASCADE, null = True, blank = True )
    beadsLabware = models.ForeignKey (
                        Beads_Labware,
                        on_delete=models.CASCADE, null = True, blank = True )
    plateLabware = models.ForeignKey (
                        Plate_Labware,
                        on_delete=models.CASCADE, null = True, blank = True )
    usedTemplateFile = models.ForeignKey(
                        ProtocolTemplateFiles,
                        on_delete=models.CASCADE)
    languageCode = models.ForeignKey(
                        Language,
                        on_delete=models.CASCADE, null = True)
    tips1000 = models.ForeignKey(
                        Tips1000_Labware,
                        on_delete=models.CASCADE, null = True)
    requestedCodeID = models.CharField(max_length = 50)
    protocolID = models.CharField(max_length = 50, default = None)
    numberOfSamples = models.CharField(max_length = 10)
    volumeBeads = models.CharField(max_length = 10)
    diluteBeads = models.BooleanField(default=None)
    resetTipcount = models.BooleanField(default=None)
    generatedFile = models.FileField(upload_to = openrobots_config.OPENROBOTS_OUTPUT_DIRECTORY )
    userNotes = models.CharField(max_length = 255)
    generatedat = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return '%s' %(self.requestedCodeID)

    def get_result_data(self):
        data = []
        data.append(self.requestedCodeID)
        data.append(self.usedTemplateFile.get_protocol_type())
        data.append(self.generatedFile)
        return data

    def get_request_info(self):
        data = []
        data.append(self.userRequestedBy.username)
        data.append(self.requestedCodeID)
        data.append(self.generatedat.strftime("%Y-%b-%d"))
        data.append(self.generatedFile)
        return data

    def get_user_file(self):
        return '%s' %(self.userRequestedBy.username)

    def get_user_file_obj(self):
        return self.userRequestedBy

    objects = RequestForStationA_Prot2Manager()


class RequestForStationA_Prot3Manager(models.Manager):

    def create_new_request (self, request_data):
        lysateLabware =  Lysate_Labware.objects.get(lysateLabwareType__exact = request_data['lysateLabware'])
        plateLabware =  Plate_Labware.objects.get(plateLabwareType__exact = request_data['plateLabware'])
        usedTemplateFile = ProtocolTemplateFiles.objects.get(protocolTemplateFileName__exact = request_data['usedTemplateFile'])
        languageCode = Language.objects.filter(languageCode__exact = request_data['languageCode']).last()
        tips1000 = Tips1000_Labware.objects.filter(tips1000 = request_data['tips1000']).last()
        new_request = self.create(userRequestedBy = request_data['userRequestedBy'], lysateLabware = lysateLabware,
                    plateLabware = plateLabware, usedTemplateFile = usedTemplateFile, languageCode = languageCode,
                    requestedCodeID = request_data['requestedCodeID'], numberOfSamples = request_data['numberOfSamples'],
                    volumeLysate = request_data['volumeLysate'], beads = util.strtobool(request_data['beads']),
                    protocolID = request_data['protocolID'] , generatedFile = request_data['generatedFile'] ,
                    resetTipcount =  util.strtobool(request_data['resetTipcount']), userNotes = request_data['userNotes'],
                    tips1000 = tips1000)

        return new_request

class RequestForStationA_Prot3 (models.Model):
    userRequestedBy = models.ForeignKey (
                        User,
                        on_delete=models.CASCADE, null = True, blank = True )
    lysateLabware = models.ForeignKey (
                        Lysate_Labware,
                        on_delete=models.CASCADE, null = True, blank = True )
    plateLabware = models.ForeignKey (
                        Plate_Labware,
                        on_delete=models.CASCADE, null = True, blank = True )
    usedTemplateFile = models.ForeignKey(
                        ProtocolTemplateFiles,
                        on_delete=models.CASCADE)
    languageCode = models.ForeignKey(
                        Language,
                        on_delete=models.CASCADE, null = True)
    tips1000 = models.ForeignKey(
                        Tips1000_Labware,
                        on_delete=models.CASCADE, null = True)
    requestedCodeID = models.CharField(max_length = 50)
    protocolID = models.CharField(max_length = 50, default = None)
    numberOfSamples = models.CharField(max_length = 10)
    volumeLysate = models.CharField(max_length = 10)
    beads = models.BooleanField()
    resetTipcount = models.BooleanField(default=None)
    generatedFile = models.FileField(upload_to = openrobots_config.OPENROBOTS_OUTPUT_DIRECTORY )
    userNotes = models.CharField(max_length = 255)
    generatedat = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return '%s' %(self.requestedCodeID)

    def get_result_data(self):
        data = []
        data.append(self.requestedCodeID)
        data.append(self.usedTemplateFile.get_protocol_type())
        data.append(self.generatedFile)
        return data

    def get_request_info(self):
        data = []
        data.append(self.userRequestedBy.username)
        data.append(self.requestedCodeID)
        data.append(self.generatedat.strftime("%Y-%b-%d"))
        data.append(self.generatedFile)
        return data

    def get_user_file(self):
        return '%s' %(self.userRequestedBy.username)

    def get_user_file_obj(self):
        return self.userRequestedBy

    objects = RequestForStationA_Prot3Manager()

class RequestForStationBManager(models.Manager):

    def create_new_request (self, request_data):
        magPlateLabware =  MagPlate_Labware.objects.get(mag_plateLabwareType__exact = request_data['magPlateLabware'])
        reagentLabware =  Reagent_Labware.objects.get(reagentLabwareType__exact = request_data['reagentLabware'])
        wasteLabware =  Waste_Labware.objects.get(wasteLabwareType__exact = request_data['wasteLabware'])
        b_elution_Labware = ElutionStationB_Labware.objects.get(elutionStationB__exact = request_data['elutionLabware'])
        usedTemplateFile = ProtocolTemplateFiles.objects.get(protocolTemplateFileName__exact = request_data['usedTemplateFile'])
        languageCode = Language.objects.filter(languageCode__exact = request_data['languageCode']).last()
        tips300 = Tips300_Labware.objects.filter(tips300 = request_data['tips300']).last()
        tips1000 = Tips1000_Labware.objects.filter(tips1000 = request_data['tips1000']).last()

        new_request = self.create(userRequestedBy = request_data['userRequestedBy'], magPlateLabware = magPlateLabware,
                    reagentLabware = reagentLabware, b_elution_Labware = b_elution_Labware, wasteLabware = wasteLabware,
                    usedTemplateFile = usedTemplateFile, requestedCodeID = request_data['requestedCodeID'], numberOfSamples = request_data['numberOfSamples'],
                    dispenseBeads = util.strtobool(request_data['dispenseBeads']), languageCode = languageCode,
                    protocolID = request_data['protocolID'], resetTipcount = util.strtobool(request_data['resetTipcount']),
                    reuseTips = util.strtobool(request_data['reuseTips']),
                    generatedFile = request_data['generatedFile'] , userNotes = request_data['userNotes'],
                    tips300 = tips300, tips1000 = tips1000)

        return new_request

class RequestForStationB (models.Model):
    userRequestedBy = models.ForeignKey (
                        User,
                        on_delete=models.CASCADE, null = True, blank = True )
    b_elution_Labware = models.ForeignKey (
                        ElutionStationB_Labware,
                        on_delete=models.CASCADE, null = True)
    magPlateLabware = models.ForeignKey (
                        MagPlate_Labware,
                        on_delete=models.CASCADE)
    reagentLabware = models.ForeignKey (
                        Reagent_Labware,
                        on_delete=models.CASCADE)
    wasteLabware = models.ForeignKey (
                        Waste_Labware,
                        on_delete=models.CASCADE)
    usedTemplateFile = models.ForeignKey(
                        ProtocolTemplateFiles,
                        on_delete=models.CASCADE)
    languageCode = models.ForeignKey(
                        Language,
                        on_delete=models.CASCADE, null = True)
    tips300 = models.ForeignKey(
                        Tips300_Labware,
                        on_delete=models.CASCADE, null = True)
    tips1000 = models.ForeignKey(
                        Tips1000_Labware,
                        on_delete=models.CASCADE, null = True)
    requestedCodeID = models.CharField(max_length = 50)
    protocolID = models.CharField(max_length = 50, default = None)
    numberOfSamples = models.CharField(max_length = 10)
    dispenseBeads = models.BooleanField()
    resetTipcount = models.BooleanField(default=None)
    reuseTips = models.BooleanField(default=None, null = True)
    generatedFile = models.FileField(upload_to = openrobots_config.OPENROBOTS_OUTPUT_DIRECTORY )
    userNotes = models.CharField(max_length = 255)
    generatedat = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return '%s' %(self.requestedCodeID)

    def get_result_data(self):
        data = []
        data.append(self.requestedCodeID)
        data.append(self.usedTemplateFile.get_protocol_type())

        data.append(self.generatedFile)
        return data
    def get_request_info(self):
        data = []
        data.append(self.userRequestedBy.username)
        data.append(self.requestedCodeID)
        data.append(self.generatedat.strftime("%Y-%b-%d"))
        data.append(self.generatedFile)
        return data

    def get_user_file(self):
        return '%s' %(self.userRequestedBy.username)

    def get_user_file_obj(self):
        return self.userRequestedBy

    objects = RequestForStationBManager()



class RequestForStationC_Prot1Manager(models.Manager):

    def create_new_request (self, request_data):

        masterMixLabware = MasterMixLabware.objects.get(MasterMixLabwareType__exact = request_data['masterMixLabware'])
        masterMixTubeLabware = MasterMixTube.objects.get(MasterMixTube__exact = request_data['masterMixTubeLabware'])
        pcrPlateLabware = PCR_plateLabware.objects.get(PCR_plateLabwareType__exact = request_data['pcrPlateLabware'])
        masterMixType = MasterMixType.objects.get(MasterMixType__exact = request_data['masterMixType'])
        c_elution_Labware = ElutionStationC_Labware.objects.get(elutionStationC__exact = request_data['c_elution_Labware'])
        station = Stations.objects.get(stationName__exact = request_data['station'])
        usedTemplateFile = ProtocolTemplateFiles.objects.get(protocolTemplateFileName__exact = request_data['usedTemplateFile'])
        languageCode = Language.objects.filter(languageCode__exact = request_data['languageCode']).last()
        tips1000 = Tips1000_Labware.objects.filter(tips1000 = request_data['tips1000']).last()

        new_request = self.create(userRequestedBy = request_data['userRequestedBy'], masterMixLabware = masterMixLabware , masterMixTubeLabware = masterMixTubeLabware,
                    pcrPlateLabware = pcrPlateLabware, c_elution_Labware = c_elution_Labware, masterMixType = masterMixType, station = station,
                    usedTemplateFile = usedTemplateFile, requestedCodeID = request_data['requestedCodeID'], numberOfSamples = request_data['numberOfSamples'],
                    prepareMastermix = util.strtobool(request_data['prepareMastermix']), languageCode = languageCode,
                    volumeElution = request_data ['volumeElution'], transferMastermix = util.strtobool(request_data['transferMastermix']),
                    protocolID = request_data['protocolID'], transferSamples = util.strtobool(request_data['transferSamples']),
                    resetTipcount =  util.strtobool(request_data['resetTipcount']),
                    generatedFile = request_data['generatedFile'] , userNotes = request_data['userNotes'],
                    tips1000 = tips1000)

        return new_request



class RequestForStationC_Prot1 (models.Model):
    userRequestedBy = models.ForeignKey (
                        User,
                        on_delete=models.CASCADE, null = True, blank = True )
    masterMixLabware = models.ForeignKey (
                        MasterMixLabware,
                        on_delete=models.CASCADE)
    masterMixTubeLabware = models.ForeignKey (
                        MasterMixTube,
                        on_delete=models.CASCADE)
    pcrPlateLabware = models.ForeignKey (
                        PCR_plateLabware,
                        on_delete=models.CASCADE)
    c_elution_Labware = models.ForeignKey (
                        ElutionStationC_Labware,
                        on_delete=models.CASCADE, null = True)
    masterMixType = models.ForeignKey (
                        MasterMixType,
                        on_delete=models.CASCADE)
    station = models.ForeignKey(
                        Stations,
                        on_delete=models.CASCADE)
    usedTemplateFile = models.ForeignKey(
                        ProtocolTemplateFiles,
                        on_delete=models.CASCADE)
    languageCode = models.ForeignKey(
                        Language,
                        on_delete=models.CASCADE, null = True)
    tips1000 = models.ForeignKey(
                        Tips1000_Labware,
                        on_delete=models.CASCADE, null = True)
    requestedCodeID = models.CharField(max_length = 50)
    protocolID = models.CharField(max_length = 50, default = None)
    numberOfSamples = models.CharField(max_length = 10)
    prepareMastermix = models.BooleanField()
    transferMastermix = models.BooleanField()
    transferSamples = models.BooleanField()
    resetTipcount = models.BooleanField(default=None)
    volumeElution = models.CharField(max_length = 10,  null = True)
    generatedFile = models.FileField(upload_to = openrobots_config.OPENROBOTS_OUTPUT_DIRECTORY )
    userNotes = models.CharField(max_length = 255)
    generatedat = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return '%s' %(self.requestedCodeID)

    def get_result_data(self):
        data = []
        data.append(self.requestedCodeID)
        data.append(self.usedTemplateFile.get_protocol_type())

        data.append(self.generatedFile)
        return data

    def get_request_info(self):
        data = []
        data.append(self.userRequestedBy.username)
        data.append(self.requestedCodeID)
        data.append(self.generatedat.strftime("%Y-%b-%d"))
        data.append(self.generatedFile)
        return data

    def get_user_file(self):
        return '%s' %(self.userRequestedBy.username)

    def get_user_file_obj(self):
        return self.userRequestedBy

    objects = RequestForStationC_Prot1Manager()
'''
class FileIDUserRequestMapping(models.Model):
    fileID = models.CharField(max_length = 50)
    station = models.CharField(max_length = 20)
    protocol = models.CharField(max_length = 50)
    generatedat = models.DateTimeField(auto_now_add=True)
'''

class RequestForStationC_Prot2Manager(models.Manager):

    def create_new_request (self, request_data):

        masterMixLabware = MasterMixLabware.objects.get(MasterMixLabwareType__exact = request_data['masterMixLabware'])
        #masterMixTubeLabware = MasterMixTube.objects.get(MasterMixTube__exact = request_data['masterMixTubeLabware'])
        pcrPlateLabware = PCR_plateLabware.objects.get(PCR_plateLabwareType__exact = request_data['pcrPlateLabware'])
        #masterMixType = MasterMixType.objects.get(MasterMixType__exact = request_data['masterMixType'])
        c_elution_Labware = ElutionStationC_Labware.objects.get(elutionStationC__exact = request_data['c_elution_Labware'])

        usedTemplateFile = ProtocolTemplateFiles.objects.get(protocolTemplateFileName__exact = request_data['usedTemplateFile'])
        languageCode = Language.objects.filter(languageCode__exact = request_data['languageCode']).last()

        new_request = self.create(userRequestedBy = request_data['userRequestedBy'], masterMixLabware = masterMixLabware ,
                    # masterMixTubeLabware = masterMixTubeLabware,
                    pcrPlateLabware = pcrPlateLabware, c_elution_Labware = c_elution_Labware,
                    # masterMixType = masterMixType, station = station,
                    usedTemplateFile = usedTemplateFile, requestedCodeID = request_data['requestedCodeID'], numberOfSamples = request_data['numberOfSamples'],
                    # prepareMastermix = util.strtobool(request_data['prepareMastermix']),
                    languageCode = languageCode, volumeElution = request_data ['volumeElution'],
                    #transferMastermix = util.strtobool(request_data['transferMastermix']),
                    protocolID = request_data['protocolID'],
                    #transferSamples = util.strtobool(request_data['transferSamples']),
                    resetTipcount =  util.strtobool(request_data['resetTipcount']),
                    generatedFile = request_data['generatedFile'] , userNotes = request_data['userNotes'])

        return new_request



class RequestForStationC_Prot2 (models.Model):
    userRequestedBy = models.ForeignKey (
                        User,
                        on_delete=models.CASCADE, null = True, blank = True )
    masterMixLabware = models.ForeignKey (
                        MasterMixLabware,
                        on_delete=models.CASCADE)
    '''
    masterMixTubeLabware = models.ForeignKey (
                        MasterMixTube,
                        on_delete=models.CASCADE)
    '''
    pcrPlateLabware = models.ForeignKey (
                        PCR_plateLabware,
                        on_delete=models.CASCADE)
    c_elution_Labware = models.ForeignKey (
                        ElutionStationC_Labware,
                        on_delete=models.CASCADE, null = True)
    '''
    masterMixType = models.ForeignKey (
                        MasterMixType,
                        on_delete=models.CASCADE)
    station = models.ForeignKey(
                        Stations,
                        on_delete=models.CASCADE)
    '''
    usedTemplateFile = models.ForeignKey(
                        ProtocolTemplateFiles,
                        on_delete=models.CASCADE)
    languageCode = models.ForeignKey(
                        Language,
                        on_delete=models.CASCADE, null = True)
    requestedCodeID = models.CharField(max_length = 50)
    protocolID = models.CharField(max_length = 50, default = None)
    numberOfSamples = models.CharField(max_length = 10)
    #prepareMastermix = models.BooleanField()
    #transferMastermix = models.BooleanField()
    #transferSamples = models.BooleanField()
    resetTipcount = models.BooleanField(default=None)
    volumeElution = models.CharField(max_length = 10,  null = True)
    generatedFile = models.FileField(upload_to = openrobots_config.OPENROBOTS_OUTPUT_DIRECTORY )
    userNotes = models.CharField(max_length = 255)
    generatedat = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return '%s' %(self.requestedCodeID)

    def get_result_data(self):
        data = []
        data.append(self.requestedCodeID)
        data.append(self.usedTemplateFile.get_protocol_type())

        data.append(self.generatedFile)
        return data

    def get_request_info(self):
        data = []
        data.append(self.userRequestedBy.username)
        data.append(self.requestedCodeID)
        data.append(self.generatedat.strftime("%Y-%b-%d"))
        data.append(self.generatedFile)
        return data

    def get_user_file(self):
        return '%s' %(self.userRequestedBy.username)

    def get_user_file_obj(self):
        return self.userRequestedBy

    objects = RequestForStationC_Prot2Manager()




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
