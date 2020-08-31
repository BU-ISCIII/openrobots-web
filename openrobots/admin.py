from django.contrib import admin
from openrobots.models import *

class StationsAdmin (admin.ModelAdmin):
    list_display =['stationName', 'description']

class ProtocolsTypeAdmin (admin.ModelAdmin):
    list_display =['protocolTypeName', 'description']

class ProtocolosInStationAdmin (admin.ModelAdmin):
    list_display = ['protocolNumber', 'station', 'typeOfProtocol']

class ProtocolTemplateFilesAdmin (admin.ModelAdmin):
    list_display =['station', 'typeOfProtocol', 'protocolTemplateFileName', 'protocolTemplateFileName',
                'authors', 'source', 'apiLevel', 'protocolNameInForm', 'parametersDefined', 'protocolTemplateBeUsed']

class ElutionHardwareAdmin (admin.ModelAdmin):
    list_display =['hardwareType']

class InventoryLabwareAdmin (admin.ModelAdmin):
    list_display =['elution_LabwareType', 'brand', 'valueInCode']

class MagPlate_Labwaredmin (admin.ModelAdmin):
    list_display =('mag_plateLabwareType', 'description', 'default')

class ModuleTypeAdmin (admin.ModelAdmin):
    list_display =('moduleType', 'description')

class ModulesInLabAdmin (admin.ModelAdmin):
    list_display =('moduleType','moduleID', 'description')



class RobotsInventoryAdmin (admin.ModelAdmin):
    list_display =('userName', 'configuration',  'location','robots', 'serialNumber','IP_address','hostName',
            'computer_mac','rightPipette', 'leftPipette', 'rightPipetteID', 'leftPipetteID', 'neededPlugs','observations')

class RobotsActionPostAdmin(admin.ModelAdmin):
    list_display = ['RobotID', 'executedAction', 'ipaddress','ProtocolID', 'StartRunTime', 'FinishRunTime','modifiedParameters']


class ParametersRobotActionAdmin(admin.ModelAdmin):
    list_display = ['robotActionPost', 'protocolID','parameterName', 'parameterValue', 'modified']

class ProtocolParameterAdmin(admin.ModelAdmin):
    list_display = ['usedTemplateFile', 'parameterType', 'parameterName', 'nameInForm', 'defaultValue']

class ParameterOptionAdmin(admin.ModelAdmin):
    list_display = ['parameter', 'optionValue', 'optionDescription', 'default']

class ProtocolRequestAdmin(admin.ModelAdmin):
    list_display = ['protocolTemplate', 'userRequestedBy', 'requestedCodeID','protocolID', 'generatedFile','stationName', 'templateProtocolNumber', 'userNotes']


class ProtocolParameterValuesAdmin(admin.ModelAdmin):
    list_display = ['protocolRequest', 'parameterName', 'parameterValue']


admin.site.register(Stations , StationsAdmin)
admin.site.register(ProtocolsType , ProtocolsTypeAdmin)
admin.site.register(ProtocolosInStation, ProtocolosInStationAdmin)
admin.site.register(ProtocolTemplateFiles , ProtocolTemplateFilesAdmin)
admin.site.register(ElutionHardware , ElutionHardwareAdmin)

admin.site.register(ModuleType , ModuleTypeAdmin)
admin.site.register(ModulesInLab , ModulesInLabAdmin)

admin.site.register(RobotsInventory , RobotsInventoryAdmin)
admin.site.register(InventoryLabware , InventoryLabwareAdmin)

admin.site.register(RobotsActionPost, RobotsActionPostAdmin)
admin.site.register(ParametersRobotAction, ParametersRobotActionAdmin)

admin.site.register(ProtocolParameter, ProtocolParameterAdmin)
admin.site.register(ParameterOption, ParameterOptionAdmin)

admin.site.register(ProtocolRequest,ProtocolRequestAdmin)
admin.site.register(ProtocolParameterValues,ProtocolParameterValuesAdmin)
