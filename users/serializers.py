from rest_framework import serializers
from .models import User
from company_service.serializers import CompanySerializer
from groups.serializers import GroupSerializer

class UserSerializer(serializers.HyperlinkedModelSerializer):
    default_company = CompanySerializer()
    groups = GroupSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'email',
            'is_active',
            'default_company',
            'groups',
            'created',
            'modified',
        )
