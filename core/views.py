from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .mixins import CSRFExemptMixin
from .models import Appointment
from .serializers import AppointmentSerializer



# Create your views here.
class AppointMentCreateAPIView(APIView):
    authentication_classes = (CSRFExemptMixin, )
    serializer_class = AppointmentSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):

        user = request.user
        data = request.data
        appointment = Appointment.objects.create(department_id=data['department'], doctor_id=data['doctor'],date=data['date'],message=data['message'])

        if user.is_anonymous == False:
            appointment.email = user.email
            appointment.phone = user.phone_number
            appointment.name = user.get_full_name()
            appointment.patient = user
        else:
            appointment.phone = data['phone']
            appointment.email = data['email']
            appointment.name = data['name']

        appointment.save()
        serializer = self.serializer_class(appointment)
        return Response(serializer.data)
            
from django.core.mail import  EmailMultiAlternatives
from django.contrib import auth, messages
from django.shortcuts import get_object_or_404, redirect,render,HttpResponse,HttpResponseRedirect


def send_contact(request):
    
    if request.method == 'POST':
        # Process the form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        subject = request.POST.get('subject')
    
    message = f'Name: {name}\nEmail: {email}\nMessage: {message}'
    email = EmailMultiAlternatives(
    subject, message, from_email=f'{email}', to=['tabibak374@gmail.com',])
    email.content_subtype = 'html'
    email.send()
    messages.success(request, "Message Sent")
    
    return HttpResponse('Thank you for your message!')
