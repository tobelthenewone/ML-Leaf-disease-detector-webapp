from rest_framework import serializers
from users.models import NewUser
from .models import Prediction,Disease

class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    user_name = serializers.CharField(required=True)
    password1 = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = NewUser
        fields = ('id', 'email', 'user_name', 'password1', 'password2', 'is_active', 'is_superuser')
        extra_kwargs = {
            'password1': {'write_only': True},
            'password2': {'write_only': True}
        }

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password1')
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class PredictionSerializer(serializers.ModelSerializer):
    diseases_summary = serializers.SerializerMethodField()

    class Meta:
        model = Prediction
        fields = '__all__'

    def get_diseases_summary(self, obj):
        return obj.get_diseases_summary()



class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'