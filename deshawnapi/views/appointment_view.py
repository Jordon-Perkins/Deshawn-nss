from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from deshawnapi.models import Appointment, Walker


class AppointmentView(ViewSet):
#if we are defining something in the class we call it a 'method' 'defingin a method on the class'
#when definging inside a class specifically
    def retrieve(self, request, pk=None): #declaring a methos that accepts the parsed path; a request and a primary key
        appointment = Appointment.objects.get(pk=pk) #gets a single appointment declaring the appointment variable and assigning to the appointment object that matches PK
        serialized = AppointmentSerializer(appointment, context={'request': request}) #declaring a variable serialized and sets it equal to the return value of the appointment serialze
        return Response(serialized.data, status=status.HTTP_200_OK) # returns a body of json stringifies object to the client, and a status code of 200 OK in the headers
#in a fuction definition in the parathensis we call those parameters
    def list(self, request):# defining a fuction with the parameters self, request
        appointments = Appointment.objects.all() #we are declaring the appointments variable and assigning it the value of a list of instances of the appointment database model, querying the appointment table in the databawse to return a list of instances of the database nmodel
        serialized = AppointmentSerializer(appointments, many=True) #declaring the serialized variable assign its' value to the return json string of the appointment serializer which takes the arguments appointments, many=true, which tells the return to expect a list of instances

        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        # Get the related walker from the database using the request body value
        client_walker_id = request.data["walkerId"]
        walker_instance = Walker.objects.get(pk=client_walker_id)

        # Create a new appointment instance
        appointment = Appointment()

        # Use Walker instance as the value of the model property
        appointment.walker = walker_instance

        # Assign the appointment date using the request body value
        appointment.date = request.data["appointmentDate"]

        # Performs the INSERT statement into the deshawnapi_appontment table
        appointment.save()

        # Serialization will be covered in the next chapter
        serialized = AppointmentSerializer(appointment, many=False)

        # Respond with the newly created appointment in JSON format with a 201 status code
        return Response(serialized.data, status=status.HTTP_201_CREATED)


# The serializer will be covered in the next chapter
class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = ('id', 'walker', 'date',)
