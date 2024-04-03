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
    follow_up_marketer = PropertyMarketerSerializer()

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

class EmailSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=200)
    message = serializers.CharField()
    media = serializers.FileField()


class CustomerConversionSerializer(serializers.Serializer):
    prospect_id = serializers.IntegerField()
    amount = serializers.IntegerField()
    receipt = serializers.FileField()
    other_files = serializers.FileField()
    payment_status = serializers.ChoiceField(choices=['completed', 'incompleted'])
    follow_up_description = serializers.CharField()

    def create(self, validated_data):
        return Customer.objects.create(**validated_data)