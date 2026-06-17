from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Doctor URLs
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/add/', views.add_doctor, name='add_doctor'),
    path('doctors/edit/<int:id>/', views.edit_doctor, name='edit_doctor'),
    path('doctors/delete/<int:id>/', views.delete_doctor, name='delete_doctor'),

    # Patient URLs
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/add/', views.add_patient, name='add_patient'),
    path('patients/edit/<int:id>/', views.edit_patient, name='edit_patient'),
    path('patients/delete/<int:id>/', views.delete_patient, name='delete_patient'),
    path('patients/history/<int:id>/', views.patient_history, name='patient_history'),

    # Appointment URLs
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/add/', views.add_appointment, name='add_appointment'),
    path('appointments/edit/<int:id>/', views.edit_appointment, name='edit_appointment'),
    path('appointments/delete/<int:id>/', views.delete_appointment, name='delete_appointment'),

    # Prescription URLs
    path('prescriptions/', views.prescription_list, name='prescription_list'),
    path('prescriptions/add/', views.add_prescription, name='add_prescription'),
    path('prescriptions/edit/<int:id>/', views.edit_prescription, name='edit_prescription'),
    path('prescriptions/delete/<int:id>/', views.delete_prescription, name='delete_prescription'),

    # Lab Report URLs
    path('lab-reports/', views.lab_report_list, name='lab_report_list'),
    path('lab-reports/add/', views.add_lab_report, name='add_lab_report'),
    path('lab-reports/download/<int:id>/', views.download_lab_report, name='download_lab_report'),
    path('lab-reports/delete/<int:id>/', views.delete_lab_report, name='delete_lab_report'),

    # AI Symptom Checker
    path('symptom-checker/', views.symptom_checker, name='symptom_checker'),
]