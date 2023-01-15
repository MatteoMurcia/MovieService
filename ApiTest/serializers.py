from rest_framework import serializers
from .models import People,Movie

class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ['id','email','password']
        
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id','name','gender','duration','objectType','puntuation','clasification','creatorEmail']