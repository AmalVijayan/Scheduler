
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
import scheduler_api.serializers
import scheduler_schema.models
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

# Create your views here.

# Single View that handles Song, Podcast and AudioBook

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = scheduler_schema.models.Schedule.objects.all()
    # serializer_class = scheduler_api.serializers.ScheduleDetailSerializer

    def get_serializer_class(self):
        
        """
        The following statement obtains the aud_type from the user depending on the type of request
        In create and update the request data contains the aud_type, all other request contains aud_type as
        a URL parameter
        """
    
        if self.action == 'create' or self.action == 'partial_update' :
            return scheduler_api.serializers.ScheduleCreateSerializer

        return scheduler_api.serializers.ScheduleDetailSerializer


    # Overriding the create method of Viewset
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        op_serialize = scheduler_api.serializers.ScheduleDetailSerializer(instance, many=False)
        return Response(op_serialize.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()
    
    # Overriding the update method of Viewset
    def partial_update(self, request, pk=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = get_object_or_404(scheduler_schema.models.Schedule, pk=pk)
        updated = serializer.update(instance, serializer.data)
        op_serialize = scheduler_api.serializers.ScheduleDetailSerializer(updated, many=False)
        return Response(op_serialize.data, status=status.HTTP_200_OK)