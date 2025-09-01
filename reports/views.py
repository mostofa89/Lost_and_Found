from django.shortcuts import render, redirect
from django.contrib import messages as messages
from django.contrib.auth.decorators import login_required
from .forms import LostReportForm
from .models import Lost_reports
# Create your views here.
@login_required
def lost_reports(request):
    if request.method == "POST":
        form = LostReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            messages.success(request, "Your lost item report has been submitted successfully.")
            return redirect('reports:lost_reports')
    else:
        form = LostReportForm()

    reports = Lost_reports.objects.all().order_by('-reported_at')
    return render(request, 'reports/lost_reports.html', {'form': form, 'reports': reports})
