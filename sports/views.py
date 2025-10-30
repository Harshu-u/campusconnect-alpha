from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def sports_view(request):
    # TODO: Add logic for sports
    context = {}
    return render(request, 'sports/sports.html', context)