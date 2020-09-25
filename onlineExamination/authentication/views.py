from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth

# Create your views here.

def login(request):

    if request.method == 'POST':

        email = request.POST['Email']
        password = request.POST['Password']
    
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/home')  
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')

    else:
        return render(request,'login.html')

def signup(request):

    first_name = request.POST['firstname']
    last_name = request.POST['lastname']
    email = request.POST['email']
    password = request.POST['password']

    if User.objects.filter(email=email).exists():
        messages.info(request, 'Email Already Registered in Database')
        return redirect('login')
    else:
        user = User.objects.create_user(username=email, password=password, email=email, first_name=first_name, last_name=last_name)
        user.save()
        auth.login(request, user)
        return redirect('/home')
    
    pass

def logout(request):
    auth.logout(request)
    return redirect('/home')
