from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import date

@login_required
def attendance_view(request):
    # TODO: Add logic for attendance based on user role
    context = {'today_date': date.today().strftime('%Y-%m-%d')}
    return render(request, 'attendance/attendance.html', context)