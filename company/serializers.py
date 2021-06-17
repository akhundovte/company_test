
from rest_framework import serializers
from .models import Company, News
from .services import create_bind_user_to_company


class CompanySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(label='Название', required=True, max_length=255)
    info = serializers.CharField(label='Описание', required=False, allow_blank=True)

    def create(self, validated_data):
        return Company.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.info = validated_data.get('info', instance.info)
        instance.save()
        return instance


class CompanyBindSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    company_id = serializers.IntegerField(required=True)

    def create(self, validated_data):
        return create_bind_user_to_company(
            user_id=validated_data['user_id'],
            company_id=validated_data['company_id'],
            )


class NewsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(label='Заголовок', required=True, max_length=255)
    content = serializers.CharField(label='Содержание', required=False, allow_blank=True)
    company_id = serializers.IntegerField(required=True)

    def create(self, validated_data):
        return News.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.company_id = validated_data.get('company_id', instance.company_id)
        instance.save()
        return instance
