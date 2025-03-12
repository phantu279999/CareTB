from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import EmployeeViewSet, CollaboratorViewSet


router = DefaultRouter()
router.register('employees', EmployeeViewSet, basename='employee')
router.register('collaborators', CollaboratorViewSet, basename='collaborator')


urlpatterns = [
    path('', include(router.urls)),
]
