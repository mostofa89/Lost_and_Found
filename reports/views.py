from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib import messages as messages
from django.contrib.auth.decorators import login_required
from .models import Lost_reports
# Create your views here.
@login_required
def lost_reports_view(request):
    if request.method == "POST":
        user = request.user
        item_name = request.POST.get('item_name')
        item_description = request.POST.get('item_description')
        date_str = request.POST.get('date_lost')
        location = request.POST.get('location')
        contact = request.POST.get('contact')
        item_image = request.FILES.get('item_image')
        try:
            date_lost = datetime.strptime(date_str, "%Y-%m-%d").date()
            report = Lost_reports(
            user=user,
            item_name=item_name,
            item_description=item_description,
            date_lost=date_lost,
            location=location,
            contact=contact,
            item_image=item_image
            )
            print(date_lost)
            report.save()
            messages.success(request, "Your lost item report has been submitted successfully.")
            return redirect('reports:lost_reports')
    
        except ValueError:
            messages.error(request, "Invalid date format. Use DD/MM/YYYY.")
            return redirect('reports:lost_reports')
       

    reports = Lost_reports.objects.all().order_by('-reported_at')
    return render(request, 'reports/lost_reports.html', {'reports': reports})

