
from rest_framework import viewsets
import scheduler_api.serializers
import scheduler_schema.models
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils.timezone import make_aware
from datetime import datetime 

# Create your views here.


"""
The following 2 funtions checks for the availablity of each user passed in the API payload
"""                                          
clean_list = lambda x : x != None

def check_user_availability(data):

    added_users = data['users']
    new_event_start = data['start_date_time']
    new_event_end = data['end_date_time']        

    new_event_start = make_aware(datetime.strptime(new_event_start, '%Y-%m-%dT%H:%M:%SZ'))
    new_event_end = make_aware(datetime.strptime(new_event_end, '%Y-%m-%dT%H:%M:%SZ'))

    check_user_availability = lambda x : scheduler_schema.models.UserAvailibility.objects.get(id=x).userNotAvailable(start_date_time=new_event_start, 
                                                                                            end_date_time=new_event_end)

    unavailable_users = list(map(check_user_availability, added_users))
    unavailable_users = list(filter(clean_list, unavailable_users))

    return unavailable_users

# View for Schedule CRUD API

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = scheduler_schema.models.Schedule.objects.all()
    # serializer_class = scheduler_api.serializers.ScheduleDetailSerializer

    def get_serializer_class(self):
        
        """
        Selecting the appropriate serializer based on the request method
        """
    
        if self.action == 'create' or self.action == 'partial_update':
            return scheduler_api.serializers.ScheduleCreateSerializer

        return scheduler_api.serializers.ScheduleDetailSerializer


    # Overriding the create method of Viewset
    def create(self, request, *args, **kwargs):

        unavailable_users = check_user_availability(request.data)

        if unavailable_users:
            return Response({"error": f"There are conflicts in the schedule", "unavailable_users" : unavailable_users}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        op_serialize = scheduler_api.serializers.ScheduleDetailSerializer(instance, many=False)
        return Response({"message":"Successfully scheduled!", "data" : op_serialize.data}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()
    
    # Overriding the update method of Viewset
    def partial_update(self, request, pk=None, *args, **kwargs):

        unavailable_users = check_user_availability(request.data)

        if unavailable_users:
            return Response({"error": f"There are conflicts in the Schedule", "unavailable_users" : unavailable_users}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = get_object_or_404(scheduler_schema.models.Schedule, pk=pk)
        updated = serializer.update(instance, serializer.data)
        op_serialize = scheduler_api.serializers.ScheduleDetailSerializer(updated, many=False)
        return Response({"message":"Successfully updated!", "data" : op_serialize.data}, status=status.HTTP_200_OK)