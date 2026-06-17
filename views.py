from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
import os

from .models import Doctor, Patient, Appointment, Prescription, LabReport
from .forms import (
    DoctorForm,
    PatientForm,
    AppointmentForm,
    PrescriptionForm,
    LabReportForm
)


# ===========================
# Dashboard
# ===========================

@login_required
def home(request):
    total_doctors = Doctor.objects.count()
    total_patients = Patient.objects.count()
    total_appointments = Appointment.objects.count()
    total_prescriptions = Prescription.objects.count()
    recent_appointments = Appointment.objects.all().order_by('-id')[:5]

    return render(request, 'hospital/home.html', {
        'total_doctors': total_doctors,
        'total_patients': total_patients,
        'total_appointments': total_appointments,
        'total_prescriptions': total_prescriptions,
        'recent_appointments': recent_appointments,
    })


# ===========================
# Doctor Management
# ===========================

@login_required
def doctor_list(request):
    query = request.GET.get('q')
    doctors = Doctor.objects.all().order_by('-id')

    if query:
        doctors = doctors.filter(
            name__icontains=query
        ) | doctors.filter(
            specialization__icontains=query
        )

    return render(request, 'hospital/doctor_list.html', {
        'doctors': doctors,
        'query': query
    })


@login_required
def add_doctor(request):
    form = DoctorForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('doctor_list')

    return render(request, 'hospital/add_doctor.html', {
        'form': form
    })


@login_required
def edit_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    form = DoctorForm(request.POST or None, instance=doctor)

    if form.is_valid():
        form.save()
        return redirect('doctor_list')

    return render(request, 'hospital/add_doctor.html', {
        'form': form
    })


@login_required
def delete_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    doctor.delete()
    return redirect('doctor_list')


# ===========================
# Patient Management
# ===========================

@login_required
def patient_list(request):
    query = request.GET.get('q')
    patients = Patient.objects.all().order_by('-id')

    if query:
        patients = patients.filter(
            name__icontains=query
        ) | patients.filter(
            phone__icontains=query
        )

    return render(request, 'hospital/patient_list.html', {
        'patients': patients,
        'query': query
    })


@login_required
def add_patient(request):
    form = PatientForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('patient_list')

    return render(request, 'hospital/add_patient.html', {
        'form': form
    })


@login_required
def edit_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    form = PatientForm(request.POST or None, instance=patient)

    if form.is_valid():
        form.save()
        return redirect('patient_list')

    return render(request, 'hospital/add_patient.html', {
        'form': form
    })


@login_required
def delete_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    patient.delete()
    return redirect('patient_list')


@login_required
def patient_history(request, id):
    patient = get_object_or_404(Patient, id=id)

    appointments = Appointment.objects.filter(
        patient=patient
    ).order_by('-id')

    prescriptions = Prescription.objects.filter(
        patient=patient
    ).order_by('-id')

    lab_reports = LabReport.objects.filter(
        patient=patient
    ).order_by('-uploaded_at')

    return render(request, 'hospital/patient_history.html', {
        'patient': patient,
        'appointments': appointments,
        'prescriptions': prescriptions,
        'lab_reports': lab_reports,
    })


# ===========================
# Appointment Management
# ===========================

@login_required
def appointment_list(request):
    status = request.GET.get('status')
    appointments = Appointment.objects.all().order_by('-id')

    if status:
        appointments = appointments.filter(status=status)

    return render(request, 'hospital/appointment_list.html', {
        'appointments': appointments,
        'status': status
    })


@login_required
def add_appointment(request):
    form = AppointmentForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('appointment_list')

    return render(request, 'hospital/add_appointment.html', {
        'form': form
    })


@login_required
def edit_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    form = AppointmentForm(request.POST or None, instance=appointment)

    if form.is_valid():
        form.save()
        return redirect('appointment_list')

    return render(request, 'hospital/add_appointment.html', {
        'form': form
    })


@login_required
def delete_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    appointment.delete()
    return redirect('appointment_list')


# ===========================
# Prescription Management
# ===========================

@login_required
def prescription_list(request):
    prescriptions = Prescription.objects.all().order_by('-id')

    return render(request, 'hospital/prescription_list.html', {
        'prescriptions': prescriptions
    })


@login_required
def add_prescription(request):
    form = PrescriptionForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('prescription_list')

    return render(request, 'hospital/add_prescription.html', {
        'form': form
    })


@login_required
def edit_prescription(request, id):
    prescription = get_object_or_404(Prescription, id=id)
    form = PrescriptionForm(request.POST or None, instance=prescription)

    if form.is_valid():
        form.save()
        return redirect('prescription_list')

    return render(request, 'hospital/add_prescription.html', {
        'form': form
    })


@login_required
def delete_prescription(request, id):
    prescription = get_object_or_404(Prescription, id=id)
    prescription.delete()
    return redirect('prescription_list')


# ===========================
# Lab Report Management
# ===========================

@login_required
def lab_report_list(request):
    reports = LabReport.objects.all().order_by('-uploaded_at')

    return render(request, 'hospital/lab_report_list.html', {
        'reports': reports
    })


@login_required
def add_lab_report(request):
    form = LabReportForm(
        request.POST or None,
        request.FILES or None
    )

    if form.is_valid():
        form.save()
        return redirect('lab_report_list')

    return render(request, 'hospital/add_lab_report.html', {
        'form': form
    })


@login_required
def download_lab_report(request, id):
    report = get_object_or_404(LabReport, id=id)

    # Make sure your model field name is report_file
    if report.report_file:
        file_path = report.report_file.path

        if os.path.exists(file_path):
            return FileResponse(
                open(file_path, 'rb'),
                as_attachment=True,
                filename=os.path.basename(file_path)
            )

    raise Http404("Lab report file not found.")


@login_required
def delete_lab_report(request, id):
    report = get_object_or_404(LabReport, id=id)
    report.delete()
    return redirect('lab_report_list')


# ===========================
# Symptom Checker
# ===========================

@login_required
def symptom_checker(request):
    result = None

    if request.method == "POST":
        symptoms = request.POST.getlist("symptoms")

        if "fever" in symptoms and "cough" in symptoms:
            result = {
                "disease": "Flu / Viral Infection",
                "department": "General Physician",
                "priority": "Medium"
            }

        elif "chest_pain" in symptoms:
            result = {
                "disease": "Possible Heart Problem",
                "department": "Cardiology",
                "priority": "High"
            }

        elif "headache" in symptoms and "vomiting" in symptoms:
            result = {
                "disease": "Migraine / Neurological Issue",
                "department": "Neurology",
                "priority": "Medium"
            }

        elif "stomach_pain" in symptoms:
            result = {
                "disease": "Digestive Problem",
                "department": "Gastroenterology",
                "priority": "Low"
            }

        elif "fever" in symptoms:
            result = {
                "disease": "General Fever / Infection",
                "department": "General Physician",
                "priority": "Low"
            }

        else:
            result = {
                "disease": "General Checkup Recommended",
                "department": "General Physician",
                "priority": "Low"
            }

    return render(request, "hospital/symptom_checker.html", {
        "result": result
    })