from django.urls import path
from . import views

app_name = "fees"

urlpatterns = [
    path("", views.fees_dashboard, name="dashboard"),
    path("defaulters/", views.defaulters_report, name="defaulters_report"),
    path("defaulters/export/", views.export_defaulters_csv, name="export_defaulters"),
    path("defaulters/remind/<int:fee_id>/", views.send_fee_reminder, name="send_reminder"),
    path("defaulters/remind-bulk/", views.send_bulk_fee_reminders, name="send_bulk_reminders"),
    path("dashboard/", views.fees_dashboard, name="fees_dashboard"),
]
