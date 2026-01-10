from django.shortcuts import redirect
from django.shortcuts import render
from django.db import models
from django.contrib import messages
from .models import Lead
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Count
from .utils import send_admin_email, send_admin_whatsapp

def home(request):
    return render(request, "pages/home.html")

def create_lead(request):
    if request.method == "POST":
        lead = Lead.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            institute=request.POST.get("institute"),
            role=request.POST.get("role"),
            city=request.POST.get("city"),

            # 🔑 THIS IS THE KEY LINE
            source=request.POST.get("source", "Home"),
        )

        # Admin notifications
        send_admin_email(lead)
        send_admin_whatsapp(lead)

        messages.success(
            request,
            "Thank you! Our team will contact you shortly."
        )

    return redirect("leads_dashboard")


def leads_dashboard(request):
    today = now().date()
    last_7_days = today - timedelta(days=7)

    total_leads = Lead.objects.count()
    today_leads = Lead.objects.filter(created_at__date=today).count()
    week_leads = Lead.objects.filter(created_at__date__gte=last_7_days).count()

    city_data = (
        Lead.objects.values("city")
        .order_by("city")
        .annotate(count=models.Count("id"))
    )

    latest_leads = Lead.objects.order_by("-created_at")[:10]

    return render(
        request,
        "leads/dashboard.html",
        {
            "total_leads": total_leads,
            "today_leads": today_leads,
            "week_leads": week_leads,
            "city_data": city_data,
            "latest_leads": latest_leads,
        },
    )

def leads_dashboard(request):
    today = now().date()
    last_7_days = today - timedelta(days=6)

    total_leads = Lead.objects.count()
    today_leads = Lead.objects.filter(created_at__date=today).count()
    week_leads = Lead.objects.filter(created_at__date__gte=last_7_days).count()

    
    city_qs = (
        Lead.objects.values("city")
        .annotate(count=Count("id"))
        .order_by("city")
    )

    city_labels = [c["city"] or "Unknown" for c in city_qs]
    city_counts = [c["count"] for c in city_qs]

    
    days = []
    day_counts = []

    for i in range(7):
        day = last_7_days + timedelta(days=i)
        days.append(day.strftime("%d %b"))
        day_counts.append(
            Lead.objects.filter(created_at__date=day).count()
        )

    latest_leads = Lead.objects.order_by("-created_at")[:10]

    return render(
        request,
        "leads/dashboard.html",
        {
            "total_leads": total_leads,
            "today_leads": today_leads,
            "week_leads": week_leads,
            "latest_leads": latest_leads,

            # charts
            "city_labels": city_labels,
            "city_counts": city_counts,
            "days": days,
            "day_counts": day_counts,
        },
    )

def create_lead(request):
    if request.method == "POST":
        lead = Lead.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            institute=request.POST.get("institute"),
            role=request.POST.get("role"),
            city=request.POST.get("city"),
        )

        # 🔔 ADMIN NOTIFICATIONS
        send_admin_email(lead)
        send_admin_whatsapp(lead)

        messages.success(
            request,
            "Thank you! Our team will contact you shortly."
        )

    return redirect("leads_dashboard")
# Create your views here.
