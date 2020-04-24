from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('', views.index, name = 'index'),
    path('createProtocolFile', views.create_protocol_file, name = 'create_protocol_file'),
    path('defineLabware', views.define_labware, name = 'define_labware'),
    path('defineRobot', views.define_robot, name = 'define_robot'),
    path('detailLabwareInventory=<int:labware_id>', views.detail_labware_inventory, name = 'detail_labware_inventory'),
    path('detailRobotInventory=<int:robot_id>', views.detail_robot_inventory, name = 'detail_robot_inventory'),
    path('displayTemplateFile=<int:p_template_id>', views.display_template_file, name = 'display_template_file'),
    path('labwareInventory', views.labware_inventory, name = 'labware_inventory'),
    path('modulesInventory', views.index, name = 'index'),
    path('uploadProtocolTemplates', views.upload_protocol_templates, name = 'upload_protocol_templates'),
    path('listOfRequests', views.index, name = 'index'),
    path('robotInventory', views.robot_inventory, name = 'robot_inventory'),
	]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
