from django import forms
from .models import Doctor, Patient, Appointment, Prescription, LabReport


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = '__all__'


class LabReportForm(forms.ModelForm):
    class Meta:
        model = LabReport
        fields = '__all__'