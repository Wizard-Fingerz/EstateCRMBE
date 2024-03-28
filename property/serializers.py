# serializers.py
from rest_framework import serializers
from .models import *


class FollowUpReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUpReport
        fields = '__all__'

class ReportFeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportFeedBack
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'


class PropertyMarketerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PropertyCountSerializer(serializers.Serializer):
    count = serializers.IntegerField()

class ProspectCountSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    closed_won = serializers.IntegerField()
    closed_lost = serializers.IntegerField()

class CustomerCountSerializer(serializers.Serializer):
    count = serializers.IntegerField()


class ProspectSerializer(serializers.ModelSerializer):
    property = PropertySerializer()

    class Meta:
        model = Prospect
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    property = PropertySerializer()

    class Meta:
        model = Customer
        fields = '__all__'


class ProspectAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prospect
        fields = ['id', 'follow_up_marketer']