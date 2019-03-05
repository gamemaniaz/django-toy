from rest_framework import serializers
from .models import (
    UploadedFile,
    Language, LanguageCounter,
    Doctype, DoctypeCounter,
    ConfLevel, ConfLevelCounter,
)


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadedFile
        fields = '__all__'


class LangSZ(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = '__all__'


class LangCountSZ(serializers.ModelSerializer):

    class Meta:
        model = LanguageCounter
        fields = '__all__'


class DoctypeSZ(serializers.ModelSerializer):

    class Meta:
        model = Doctype
        fields = '__all__'


class DoctypeCountSZ(serializers.ModelSerializer):

    class Meta:
        model = DoctypeCounter
        fields = '__all__'


class ConfLevelSZ(serializers.ModelSerializer):

    class Meta:
        model = ConfLevel
        fields = '__all__'


class ConfLevelCountSZ(serializers.ModelSerializer):

    class Meta:
        model = ConfLevelCounter
        fields = '__all__'
