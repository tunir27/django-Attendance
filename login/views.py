from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

from att_app.forms import RegistrationForm


def login_user(request):
    form = RegistrationForm()
    logout(request) #logs out user upon reaching the /login/ page

    std_id = password = ''
    if request.POST:
        form = RegistrationForm(request.POST or None)
        std_id = request.POST.get('std_id')
        password = request.POST.get('password')
        user = authenticate(sid=std_id, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = std_id
            return redirect('/home/att')
        else:
            messages.error(request, 'Invalid login credentials')
    return render(request,'index.html', {
        'std_id': std_id,
        'form': form,
    })

def logout_user(request):
    logout(request)
    return render(request,'index.html',{'state':'Successfully Logged Out'})

