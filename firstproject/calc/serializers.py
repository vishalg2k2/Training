from rest_framework import serializers
from.models import Traveller,Guide
from django.contrib.auth.models import User

class TravellerSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model=Traveller
        fields=['Aadhar','Name','Email','Phone','guide','owner']
    
class GuideSerializer(serializers.ModelSerializer):
    class Meta:
        model=Guide
        fields="__all__"       

class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Traveller.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']

class Traveller2Serializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model=Traveller
        fields=['Aadhar','Name','owner']
