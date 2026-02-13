from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Count
from django.contrib.auth.decorators import login_required

from .models import Lead
from .utils import send_admin_email, send_admin_whatsapp


# 🔹 Public Home Page
def home(request):
    return render(request, "pages/home.html")


# 🔹 Leads List (Sidebar: leads:list)
@login_required
def leads_list(request):
    leads = Lead.objects.all().order_by("-created_at")

    context = {
        "leads": leads,
        "total_leads": leads.count(),
    }

    return render(request, "leads/list.html", context)


# 🔹 Create Lead (Public Form)
def create_lead(request):
    if request.method == "POST":
        lead = Lead.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            institute=request.POST.get("institute"),
            role=request.POST.get("role"),
            city=request.POST.get("city"),
            source=request.POST.get("source", "Website"),
        )

        # 🔔 Admin Notifications
        send_admin_email(lead)
        send_admin_whatsapp(lead)

        messages.success(
            request,
            "Thank you! Our team will contact you shortly."
        )

        return redirect("leads:leads_dashboard")

    return redirect("home")


# 🔹 Leads Dashboard (Analytics)
@login_required
def leads_dashboard(request):
    today = now().date()
    last_7_days = today - timedelta(days=6)

    total_leads = Lead.objects.count()
    today_leads = Lead.objects.filter(created_at__date=today).count()
    week_leads = Lead.objects.filter(created_at__date__gte=last_7_days).count()

    # 📊 City-wise Data
    city_qs = (
        Lead.objects.values("city")
        .annotate(count=Count("id"))
        .order_by("city")
    )

    city_labels = [c["city"] or "Unknown" for c in city_qs]
    city_counts = [c["count"] for c in city_qs]

    # 📈 Last 7 Days Data
    days = []
    day_counts = []

    for i in range(7):
        day = last_7_days + timedelta(days=i)
        days.append(day.strftime("%d %b"))
        day_counts.append(
            Lead.objects.filter(created_at__date=day).count()
        )

    latest_leads = Lead.objects.order_by("-created_at")[:10]

    context = {
        "total_leads": total_leads,
        "today_leads": today_leads,
        "week_leads": week_leads,
        "latest_leads": latest_leads,
        "city_labels": city_labels,
        "city_counts": city_counts,
        "days": days,
        "day_counts": day_counts,
    }

    return render(request, "leads/dashboard.html", context)
