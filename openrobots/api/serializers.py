from rest_framework import serializers
from openrobots.models import RobotsActionPost

class RobotsActionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = RobotsActionPost
        fields = ['hostname','RobotID','executedAction','ProtocolID','StartRunTime','FinishRunTime']
