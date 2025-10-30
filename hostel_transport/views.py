from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def hostel_view(request):
    # TODO: Add logic for hostel/transport
    context = {}
    return render(request, 'hostel_transport/hostel.html', context)