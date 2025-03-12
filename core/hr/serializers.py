from rest_framework import serializers
from .models import Employee, Collaborator


class EmployeeSerializer(serializers.ModelSerializer):
    contract_duration = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            'id', 'code', 'full_name', 'phone', 'email', 'department',
            'position', 'contract_file', 'contract_type',
            'contract_term_start_date', 'contract_term_end_date', 'contract_duration',
            'status', 'start_date', 'gender', 'education_level'
        ]

    def get_contract_duration(self, obj):
        return obj.contract_duration()

    def validate(self, data):
        if 'contract_term_start_date' in data and 'contract_term_end_date' in data:
            if data['contract_term_end_date'] < data['contract_term_start_date']:
                raise serializers.ValidationError("End date must be after start date")
        return data


class CollaboratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collaborator
        fields = ['id', 'code', 'full_name', 'phone', 'email', 'gender', 'address']
