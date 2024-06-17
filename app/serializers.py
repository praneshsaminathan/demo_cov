from rest_framework import serializers
from .models import Covid19Data, TimeSeriesData, FileUpload, Comment

class Covid19DataSerializer(serializers.ModelSerializer):
    """
    Serializer for the Covid19Data model.
    Serializes all fields in the model.
    """
    class Meta:
        model = Covid19Data  # Specify the model to serialize
        fields = '__all__'  # Serialize all fields in the model

class TimeSeriesDataSerializer(serializers.ModelSerializer):
    """
    Serializer for the TimeSeriesData model.
    Serializes all fields in the model.
    """
    class Meta:
        model = TimeSeriesData  # Specify the model to serialize
        fields = '__all__'  # Serialize all fields in the model

class FileUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for the FileUpload model.
    Serializes all fields in the model.
    """
    class Meta:
        model = FileUpload  # Specify the model to serialize
        fields = '__all__'  # Serialize all fields in the model
        

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    Serializes all fields in the model.
    """
    
    class Meta:
        model = Comment
        fields = '__all__'
