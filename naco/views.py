# views.py
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST


@require_POST
def user_logout_view(request):
    logout(request)
    return redirect('user_logout_done')


def user_logout_done(request):
    return render(request, 'registration/user_logout.html')
