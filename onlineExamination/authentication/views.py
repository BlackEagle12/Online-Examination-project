from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
# Create your views here.

def login(request):

    if request.method == 'POST':

        email = request.POST['Email']
        password = request.POST['Password']
    
        user = auth.authenticate(username=email, password=password)
        print(user)
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
        user = User.objects.create_user(username=email, password=password, email=email, first_name=first_name, last_name=last_name, is_active=False)
        user.save()
        text = "click here http://127.0.0.1:8000/auth/emailConformation?id=" + user.id + " to conform your Email account"
        sendMail(email,"Conformation Link",text)
        return redirect('login')

    pass

def logout(request):
    auth.logout(request)
    return redirect('/home')

def emailConformation(request):
    username = request.GET['username']
    user = User.objects.get(username=username)
    user.is_active = True
    user.save()
    auth.login(request, user)
    return redirect('/home')

def sendMail(receiver_email,subject,text):
    sender_email = "vickykumar.manavadariya103232@marwadiuniversity.ac.in"
    password = "*********" ## enter email password instad of ***

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    # text = """\
    # Hi,
    # How are you?
    # """

    # Turn these into plain/html MIMEText objects
    # part2 = MIMEText(text, "plain")
    part1 = MIMEText(text, "plain")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    # message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
<<<<<<< HEAD

def forgetPassword(request):

    if request.method == 'GET':
        return render(request, 'forgetpassword.html', {'action': 'Enter email'});
    if request.method == 'POST':
        Email = request.POST['Email'];
        try:
            user = User.objects.get(email=Email)
            pin = random.randint(999, 9999)
            text = 'YOUR OTP TO RESET PASSWORD IS :' + str(pin) + ' It Will Stay active for 3 minute'
            sendMail(Email,"Forget Password", text)
            return render(request, 'forgetpassword.html', {'pin':pin, 'action': 'Conform OTP', 'id': user.id});

        except User.DoesNotExist:
            messages.info(request, 'We don\'t have any user with given Email')
            return redirect('../auth/forgetPassword')

def changepassword(request):
    if (request.method == 'POST'):
        id = request.POST['id'];
        password = request.POST['password'];

        user = User.objects.get(id=id)
        user.set_password(str(password))
        user.save()
        auth.login(request, user)
    return redirect('/home')
=======
>>>>>>> 07d17246639fa4a3c4f7057885cce46d0f2cc39c
