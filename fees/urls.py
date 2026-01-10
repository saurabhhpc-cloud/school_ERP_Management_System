from django.urls import path
from . import views
from .views import defaulters_report, export_defaulters_csv, send_fee_reminder, send_bulk_fee_reminders

urlpatterns = [
    path("", views.fees_dashboard, name="fees_dashboard"),  # 👈 ROOT
    path("defaulters/", views.defaulters_report, name="defaulters_report"),
    path("defaulters/export/", views.export_defaulters_csv, name="export_defaulters_csv"),
    path("defaulters/remind/<int:fee_id>/", views.send_fee_reminder, name="send_fee_reminder"),
    path("defaulters/remind-bulk/", views.send_bulk_fee_reminders, name="send_bulk_fee_reminders"),
]
