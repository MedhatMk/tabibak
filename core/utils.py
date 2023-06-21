import africastalking
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.contrib import auth, messages
from django.shortcuts import get_object_or_404, redirect

from core.models import Appointment

api_key = settings.AT_KEY
sender = settings.AT_SHORTCODE
username = settings.AT_USERNAME
africastalking.initialize(username, api_key)
sms = africastalking.SMS


from django.core.mail import  EmailMultiAlternatives

def mark_appointment_as_confirmed(request, pk):
    current_site = get_current_site(request)
    user = request.user
    appointment = get_object_or_404(Appointment, id=pk)
    appointment.status = 'confirmed'
    appointment.confirmed_by = user
    appointment.save()
    humanized_date = appointment.date.strftime("%Y-%m-%d %H:%M:%S")
    subject = 'Appointment Confirmed'
    message = f"Hey, {appointment.name}.Your appointment has been confirmed, please visit Dr. {appointment.doctor} on {humanized_date}, regards, {current_site.name}."
    email = EmailMultiAlternatives(
    subject, message, from_email='tabibak@proton.me', to=[appointment.email, ])
    email.content_subtype = 'html'
    email.send()

    
    messages.success(request, "Appointment Confirmed")
    if user.role == 'admin' or user.role == 'staff':
        return redirect('dashboard:appointments:appointment_details', pk=pk)
    return redirect("doctor_dashboard:appointments:appointment_details", pk=pk)





# def mark_appointment_as_confirmed(request, pk):
#     current_site = get_current_site(request)
#     user = request.user
#     appointment = get_object_or_404(Appointment, id=pk)
#     appointment.status = 'confirmed'
#     appointment.confirmed_by = user
#     appointment.save()
#     humanized_date = appointment.date.strftime("%Y-%m-%d %H:%M:%S")
#     sms.send(f"Hey, {appointment.name}.Your appointment has been confirmed, please visit the hospital on {humanized_date}, regards, {current_site.name}.", [
#              f"{appointment.phone}"], sender)
#     messages.success(request, "Appointment Confirmed")
#     if user.role == 'admin' or user.role == 'staff':
#         return redirect('dashboard:appointments:appointment_details', pk=pk)
#     return redirect("doctor_dashboard:appointments:appointment_details", pk=pk)






def mark_appointment_as_declined(request, pk):

    current_site = get_current_site(request)
    user = request.user
    appointment = get_object_or_404(Appointment, id=pk)
    appointment.status = 'declined'
    appointment.confirmed_by = user
    appointment.save()
    subject = 'Appointment Declined'
    message = f"Hey, {appointment.name}.Your appointment has been declined, please contact  Dr. {appointment.doctor} to book another appointment at a convenient date and time, regards"
    email = EmailMultiAlternatives(
    subject, message, from_email='tabibak@proton.me', to=[appointment.email, ])
    email.content_subtype = 'html'
    email.send()

    
    messages.success(request, "Appointment Declined")
    if user.role == 'admin' or user.role == 'staff':
        return redirect('dashboard:appointments:appointment_details', pk=pk)
    return redirect("doctor_dashboard:appointments:appointment_details", pk=pk)


# def mark_appointment_as_declined(request, pk):
#     current_site = get_current_site(request)
#     user = request.user
#     appointment = get_object_or_404(Appointment, id=pk)
#     appointment.status = 'declined'
#     appointment.confirmed_by = user
#     appointment.save()

#     sms.send(f"Hey, {appointment.name}.Your appointment has been declined, please contact the hospital to book another appointment at a convenient date and time, regards, {current_site.name}.", [
#              f"{appointment.phone}"], sender)
#     messages.success(request, "Appointment Declined")
#     if user.role == 'admin' or user.role == 'staff':
#         return redirect('dashboard:appointments:appointment_details', pk=pk)
#     return redirect("doctor_dashboard:appointments:appointment_details", pk=pk)

