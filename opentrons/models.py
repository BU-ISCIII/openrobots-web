from django.db import models

from django.contrib.auth.models import User
from . import opentrons_config #OPENTRONS_TEMPLATE_DIRECTORY, OPENTRONS_OUTPUT_DIRECTORY
import distutils

class Stations (models.Model):
    stationName = models.CharField(max_length = 80)
    description = models.CharField(max_length = 255, null = True, blank = True )

    def __str__ (self):
        return '%s' %(self.stationName)

    def get_station_name(self):
        return '%s' %(self.stationName)


class ModuleType (models.Model):
    moduleType = models.CharField(max_length = 20)
    description = models.CharField(max_length = 255, null = True, blank = True)

class ModulesInLab (models.Model):
    moduleType = models.ForeignKey(
                        ModuleType,
                        on_delete=models.CASCADE)
    moduleID = models.CharField(max_length = 30)
    description = models.CharField(max_length =255, null = True, blank = True)

    def __str__ (self):
        return '%s' %(self.moduleType)

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
    RP_ID = models.CharField(max_length = 20, null = True, blank = True)
    LP_ID = models.CharField(max_length = 255, null = True, blank = True)
    Module_1_ID = models.CharField(max_length = 255, null = True, blank = True)
    Module_2_ID = models.CharField(max_length = 255, null = True, blank = True)
    neededPlugs  = models.CharField(max_length = 255, null = True, blank = True)
    observations = models.CharField(max_length = 255, null = True, blank = True)

    def __str__ (self):
        return '%s' %(self.robots)

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
                    prepareMasterMix = protocol_data['prepare_mastermix'],transferMasterMix= protocol_data['transfer_mastermix'],
                    transferSamples= protocol_data['transfer_samples'])
        return new_protocol_template

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
    protocolTemplateFileName = models.FileField(upload_to = opentrons_config.OPENTRONS_TEMPLATE_DIRECTORY )
    protocolName = models.CharField(max_length = 255)
    authors = models.CharField(max_length = 255)
    source = models.CharField(max_length = 255)
    apiLevel = models.CharField(max_length = 50)
    prepareMasterMix = models.BooleanField(default = False)
    transferMasterMix = models.BooleanField(default = False)
    transferSamples = models.BooleanField(default = False)
    generatedat = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return '%s' %(self.protocolTemplateFileName)

    def get_protocol_file_name(self):
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
        data.append(self.protocolTemplateFileName)
        return data

    def get_metadata(self):
        data = []
        data.append(self.protocolName)
        data.append(self.authors)
        data.append(self.source)
        data.append(self.apiLevel)
        return data

    def get_functions(self):
        data = []
        data.append(self.prepareMasterMix)
        data.append(self.transferMasterMix)
        data.append(self.transferSamples)
        return data

    objects = ProtocolTemplateFilesManager()

class ElutionHardware (models.Model):
    hardwareType = models.CharField(max_length = 80)

    def __str__ (self):
        return '%s' %(self.hardwareType)

class MasterMixType (models.Model):
    MasterMixType = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255, null = True, blank = True )

    def __str__ (self):
        return '%s' %(self.MasterMixType)

    def get_master_mix_type (self):
        return '%s' %(self.MasterMixType)

class MasterMixLabware (models.Model):
    MasterMixLabwareType = models.CharField(max_length = 80)
    description = models.CharField(max_length = 255)

    def __str__ (self):
        return '%s' %(self.MasterMixLabwareType)

    def get_mastermix_labware_type (self):
        return '%s' %(self.MasterMixLabwareType)

class MasterMixTube (models.Model):
    MasterMixTube = models.CharField(max_length = 80)
    MasterMixRadius = models.CharField(max_length = 80)

    def __str__ (self):
        return '%s' %(self.MasterMixTube)
    def get_mastermix_tube (self):
        return '%s' %(self.MasterMixTube)

class PCR_plateLabware (models.Model):
    PCR_plateLabwareType = models.CharField(max_length = 80)
    description = models.CharField(max_length = 255)

    def __str__ (self):
        return '%s' %(self.PCR_plateLabwareType)

    def get_pcr_plate_labware_type (self):
        return '%s' %(self.PCR_plateLabwareType)

class Elution_Labware (models.Model):
    elutionHW_type =  models.ForeignKey (
                        ElutionHardware,
                        on_delete=models.CASCADE, max_length = 80, null = True, blank = True )
    elution_LabwareType = models.CharField(max_length = 80)
    description = models.CharField(max_length = 255)


    def __str__ (self):
        return '%s' %(self.elution_LabwareType)

    def get_elution_labware_type (self):
        return '%s' %(self.elution_LabwareType)

class RequestOpenTronsFilesManager(models.Manager):

    def create_new_request (self, request_data):

        masterMixLabware = MasterMixLabware.objects.get(MasterMixLabwareType__exact = request_data['masterMixLabware'])
        masterMixTubeLabware = MasterMixTube.objects.get(MasterMixTube__exact = request_data['masterMixTubeLabware'])
        pcrPlateLabware = PCR_plateLabware.objects.get(PCR_plateLabwareType__exact = request_data['pcrPlateLabware'])
        masterMixType = MasterMixType.objects.get(MasterMixType__exact = request_data['masterMixType'])
        elutionLabware = Elution_Labware.objects.get(elution_LabwareType__exact = request_data['elutionLabware'])
        station = Stations.objects.get(stationName__exact = request_data['station'])
        usedTemplateFile = ProtocolTemplateFiles.objects.get(protocolTemplateFileName__exact = request_data['usedTemplateFile'])

        new_request = self.create(userRequestedBy = request_data['userRequestedBy'], masterMixLabware = masterMixLabware , masterMixTubeLabware = masterMixTubeLabware,
                    pcrPlateLabware = pcrPlateLabware, elutionLabware = elutionLabware, masterMixType = masterMixType, station = station,
                    usedTemplateFile = usedTemplateFile, requestedCodeID = request_data['requestedCodeID'], numberOfSamples = request_data['numberOfSamples'],
                    prepareMastermix = distutils.util.strtobool(request_data['prepareMastermix']),
                    transferMastermix = distutils.util.strtobool(request_data['transferMastermix']),
                    transferSamples = distutils.util.strtobool(request_data['transferSamples']),
                    generatedFile = request_data['generatedFile'] , userNotes = request_data['userNotes'])

        return new_request


class RequestOpenTronsFiles (models.Model):
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
    elutionLabware = models.ForeignKey (
                        Elution_Labware,
                        on_delete=models.CASCADE)
    masterMixType = models.ForeignKey (
                        MasterMixType,
                        on_delete=models.CASCADE)
    station = models.ForeignKey(
                        Stations,
                        on_delete=models.CASCADE)
    usedTemplateFile = models.ForeignKey(
                        ProtocolTemplateFiles,
                        on_delete=models.CASCADE)
    requestedCodeID = models.CharField(max_length = 50)
    numberOfSamples = models.CharField(max_length = 10)
    prepareMastermix = models.BooleanField()
    transferMastermix = models.BooleanField()
    transferSamples = models.BooleanField()

    generatedFile = models.FileField(upload_to = opentrons_config.OPENTRONS_OUTPUT_DIRECTORY )
    userNotes = models.CharField(max_length = 255)
    generatedat = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return '%s' %(self.requestedCodeID)

    def get_result_data(self):
        data = []
        data.append(self.requestedCodeID)
        data.append(self.usedTemplateFile.get_protocol_type())
        data.append(self.station.get_station_name())
        data.append(self.generatedFile)
        return data

    objects = RequestOpenTronsFilesManager()
