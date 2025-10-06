from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.contrib import messages as messages
from django.contrib.auth.decorators import login_required
from .models import Lost_reports,Found_reports, Claimed_items
import re
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
            report.save()
            messages.success(request, "Your lost item report has been submitted successfully.")
            return redirect('reports:lost_reports')
    
        except ValueError:
            messages.error(request, "Invalid date format. Use DD/MM/YYYY.")
            return redirect('reports:lost_reports')
       

    reports = Lost_reports.objects.filter(user=request.user).order_by('-reported_at')
    
    return render(request, 'reports/lost_reports.html', {'reports': reports})



def found_reports_view(request):
    if request.method == "POST":
        user = request.user
        item_name = request.POST.get('item_name')
        item_description = request.POST.get('item_description')
        date_str = request.POST.get('date_found')
        location = request.POST.get('location')
        contact = request.POST.get('contact')
        item_image = request.FILES.get('item_image')
        try:
            date_lost = datetime.strptime(date_str, "%Y-%m-%d").date()
            report = Found_reports(
            user=user,
            item_name=item_name,
            item_description=item_description,
            date_lost=date_lost,
            location=location,
            contact=contact,
            item_image=item_image
            )

            report.save()
            messages.success(request, "Your found item report has been submitted successfully.")
            return redirect('reports:found_reports')
        

        except ValueError:
            messages.error(request, "Invalid date format. Use DD/MM/YYYY.")
            return redirect('reports:found_reports')
    
    reports = Found_reports.objects.filter(user=request.user).order_by('-reported_at')
    return render(request, 'reports/found_reports.html', {'reports': reports})



def inventory_view(request):
    lost_reports = Lost_reports.objects.all().order_by('-reported_at')
    found_reports = Found_reports.objects.all().order_by('-reported_at')
    return render(request, 'reports/inventory.html', {'lost_reports': lost_reports, 'found_reports': found_reports})



def claim_view(request, pk):
    found_report = get_object_or_404(Found_reports, pk=pk)

    if request.method == "POST":
        name = request.POST.get('claimant_name')
        contact = request.POST.get('claimant_contact')
        description = request.POST.get('description')

        des_list = re.findall(r'\w+', description.lower())
        report_desList = re.findall(r'\w+', found_report.item_description.lower())
        counter = sum(1 for word in des_list if word in report_desList)
        print(counter, des_list, report_desList)

        # Threshold logic
        threshold = 1
        length = len(report_desList)
        if length <= 4:
            threshold = length
        elif length <= 8:
            threshold = length / 2
        elif length <= 15:
            threshold = length / 3

        if counter >= threshold:
            claim_report = Claimed_items(
                found_report=found_report,
                item_name=found_report.item_name,
                name=name,
                contact=contact,
                description=description
            )
            print(counter, threshold)
            claim_report.save()
            messages.success(request, "✅ Your claim has been submitted successfully.")
        else:
            messages.error(request, "⚠️ Your description does not match enough with the item's description.")

        return redirect('reports:inventory')

    return render(request, 'reports/claim.html', {'found_report': found_report})

