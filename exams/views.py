from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def exams_view(request):
    # TODO: Add logic for exams
    context = {}
    return render(request, 'exams/exams.html', context)