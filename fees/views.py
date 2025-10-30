from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def fees_view(request):
    # TODO: Add logic for fees
    context = {}
    return render(request, 'fees/fees.html', context)