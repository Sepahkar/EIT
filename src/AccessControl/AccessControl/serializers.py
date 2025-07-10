from rest_framework import serializers
from .models import (
    AppTeam,
    App,
    Server,
    System,
    AppURL,
)
from InternalAccess.models import AppInfo


class AppTeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppTeam
        fields = (
            'TeamCode',
        )


class AllAppsInfoSerializer(serializers.ModelSerializer):
    FullUrl = serializers.ReadOnlyField()
    class Meta:
        model = AppInfo
        fields = (
            'AppName',
            'APPIP',
            'APPPORT',
            'APPSCHEMA',
            'FullUrl',
        )


class AppUrlSerializer(serializers.ModelSerializer):
    APPPORT = serializers.SerializerMethodField()

    class Meta:
        model = AppURL
        fields = [item.name for item in AppURL._meta.fields]
        fields.append("APPPORT")

    def get_APPPORT(self, obj):
        return obj.AppCode.SystemCode.PortNumber


class SystemSerializer(serializers.ModelSerializer):

    class Meta:
        model = System
        fields = '__all__'


class ServerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Server
        fields = '__all__'


class AppBySystemCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = App
        fields = '__all__'


class AppByAppCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = App
        fields = '__all__'


class AppSerializer(serializers.ModelSerializer):

    class Meta:
        model = App
        fields = '__all__'