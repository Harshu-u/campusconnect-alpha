from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def library_view(request):
    # TODO: Add logic for library
    context = {}
    return render(request, 'library/library.html', context)