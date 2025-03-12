from rest_framework.viewsets import ModelViewSet

from .models import Employee, Collaborator
from .serializers import EmployeeSerializer, CollaboratorSerializer


class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class CollaboratorViewSet(ModelViewSet):
    queryset = Collaborator.objects.all()
    serializer_class = CollaboratorSerializer

