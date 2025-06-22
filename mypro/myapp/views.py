from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from mypro import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token
from .models import *
import random
import string

def index(request):
    item=AddItemAdmin.objects.all()
    context = {"variable": "hello",'item':item}
    return render(request, 'index.html', context)

def menu(request):
    return render(request, 'menu.html')
def booksuccess(request):
    return render(request, 'booksuccess.html')

def about(request):
    return render(request, 'about.html')

def book(request):
    return render(request, 'book.html')

def coff(request):
    return render(request, 'mycoff.html')

def cart(request):
    return render(request, 'cart.html')


def home(request):
    return render(request, "authentication/index.html")


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')

        myuser = User.objects.create(username=username, email=email, password=pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.is_active = False
        myuser.save()
        reg=Reg.objects.create(user_id=myuser.id)
        reg.save()
        messages.success(request,
                         "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")

        # Welcome Email
        subject = "Welcome to HustleHut- Django Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to HustleHut!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nPARTH SHAH"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @HustleHut - Django Login!!"
        message2 = render_to_string('email_confirmation.html', {

            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('signin')

    return render(request, "authentication/signup.html")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request, 'activation_failed.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            # messages.success(request, "Logged In Sucessfully!!")
            return render(request, "authentication/index.html", {"fname": fname})
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')

    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return render(request,"index.html")



def generate_random_string(length):
    return ''.join(random.choice(string.digits) for _ in range(length))


def booktable(request):
    myuser = book_table.objects.all()

    if request.method == "POST":
        name = request.POST['name']
        phone_no = request.POST['phone_no']
        email = request.POST['email']
        person = request.POST['person']
        date = request.POST['date']
        random_string = generate_random_string(6)


        myuser=book_table.objects.create(
            name=name,
            phone_no=phone_no,
            email=email,
            person=person,
            date=date,
            random_string=random_string,

        )
        # myuser.is_active = False
        myuser.is_active = False
        myuser.save()

        subject = "Welcome to HustleHut- Django Login!!"
        message = "Hello " + myuser.name + "!! \n" + "Welcome to HustleHut!! \nThank you for visiting our website\n. Thank you for booking a table with us.\nYour booking reference is: " + random_string + " \n\nThanking You\nPARTH SHAH"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)


        # Email Address Confirmation Email
        # current_site = get_current_site(request)
        # email_subject = "Confirm your Email @HustleHut - Django Login!!"
        # message2 = render_to_string('email_confirmation.html', {
        #
        #     'name': myuser.first_name,
        #     'domain': current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
        #     'token': generate_token.make_token(myuser)
        # })
        # email = EmailMessage(
        #     email_subject,
        #     message2,
        #     settings.EMAIL_HOST_USER,
        #     [myuser.email],
        # )
        # email.fail_silently = True
        # email.send()

        return redirect('/booksuccess.html/')

    return render(request, "book.html")


def otp(request):
    if request.method == 'POST':
        otp1 = generate_random_string(6)
        e = request.POST.get('email')
        print(e, otp1)

        obj = User.objects.filter(email=e).exists()
        user = User.objects.filter(email=e).values('id')
        print(obj, user)

        for i in user:
            u = i.get('id')
            print(u)

            if obj is not None:
                data = Reg.objects.filter(user=u).update(otp=otp1)
                subject = "Welcome to HustleHut!!"
                message = "Hello !! \n" + "Your otp is : " + str(otp1) + "\nWelcome to HustleHut! 🎉 We're excited to have you join us." + ". 🍽️ Your dining experience is about to begin! " + " .🕒🍴\n\n"  + "\n" + "Thanking You,\n" + "PARTH SHAH"
                from_email = settings.EMAIL_HOST_USER
                to_list = [e,]
                send_mail(subject, message, from_email, to_list, fail_silently=True)
                return render(request, 'otp.html')


            else:
                messages.info(request, "Given credential is wrong...Plese check and try again")
                return render(request, 'forget.html')




    # Welcome Email



def reset(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']


        if pass1 == pass2:

             user1 = Reg.objects.filter(otp = otp).values('user')
             print(user1)

             for i in user1:
                 a = i.get('user')
                 print(a)

                 if User.objects.get(id = a):
                     b =  User.objects.get(id = a)
                     b.set_password(pass1)
                     b.save()
                     return redirect('signin')


    return render(request,'authentication/signin.html')


def forget(request):
    return render(request,"authentication/forget.html")



