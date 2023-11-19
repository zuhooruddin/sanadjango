from rest_framework import serializers
from .models import *

class ItemsSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='userid.username')
    user_email = serializers.EmailField(source='userid.email')
    user_phone= serializers.IntegerField(source='userid.phone_number')
    user_image= serializers.ImageField(source='userid.image')
    class Meta:
            model = Items
            fields = ['id', 'category', 'title', 'quantity', 'price', 'description', 'userid', 'status', 'date', 'location', 'images', 'user_name', 'user_email', 'user_phone', 'user_image']
        

   
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'image')
