from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path("CreateProfile.html", views.CreateProfile, name="CreateProfile"),
	       path("CreateProfileData", views.CreateProfileData, name="CreateProfileData"),
	       path("Hospital.html", views.Hospital, name="Hospital"),
	       path("HospitalLogin", views.HospitalLogin, name="HospitalLogin"),
	       path("AccessData.html", views.AccessData, name="AccessData"),
	       path("PatientDataAccess", views.PatientDataAccess, name="PatientDataAccess"),
	       path("PatientDetails.html", views.PatientDetails, name="PatientDetails"),
	       path("Patient.html", views.Patient, name="Patient"),
	       path("update", views.update, name="update"),
	       path("PatientLogin", views.PatientLogin, name="PatientLogin"),
	       path("edit", views.edit, name="edit"),
	       path("edit1.html", views.edit1, name="edit1"),

]