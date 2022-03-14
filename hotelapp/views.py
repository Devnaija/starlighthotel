from django.shortcuts import render

# Create your views here.
import uuid 
import json
import requests

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

from . models import Category, Room, Booking, Client, Payment
from . forms import SignupForm
from datetime import date


# Create your views here.
def index(request):
    available = Room.objects.filter(available=True)

    context = {
        'available':available
    }

    return render(request, 'index.html', context)

def categories(request):
    categories = Category.objects.all()

    context = {
        'categories':categories
    }

    return render(request, 'categories.html', context)

def single_category(request,id):
    category = Room.objects.filter(category_id=id)

    context={
        'category':category
    }

    return render(request, 'categoryroom.html', context)    

def rooms(request):
    rooms = Room.objects.all().filter(available=True)

    context={
        'rooms':rooms
    }
    return render( request, 'allrooms.html', context)
   
def single_room(request,id):
    details = Room.objects.get(pk=id)

    context={
        'details':details
    }

    return render(request, 'details.html', context)

def logoutt(request):
    logout(request)
    return redirect('signin')

def loginform(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}!')
            # subject = 'New Booking'
            # message = f'There is a new booking from {user.first_name} with contact Number {user.phone}'
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = [user.email, ]
            # send_mail( subject, message, email_from, recipient_list)
            return redirect('index')
        else:
            messages.info(request, 'Username or password incorrect. Please try again.')
            return redirect('signin')
            
    return render(request, 'signin.html')   

def signupform(request):
    reg = SignupForm()
    if request.method=='POST':
        phone = request.POST['phone']
        reg = SignupForm(request.POST)
        if reg.is_valid():
            newuser = reg.save()
            client = Client(user= newuser)
            client.first_name = newuser.first_name
            client.last_name = newuser.last_name
            client.phone = phone
            client.save()
            login(request,newuser)
            messages.success(request, f'Thank you for joining Starlight {newuser.first_name}')
            return redirect('index')
        else:
            messages.warning(request, reg.errors)
            return redirect('signup')        
    
    context ={
        'reg':reg
    }

    return render(request, 'signup.html', context)

def password(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password updated successfully!')
            return redirect('history')
        else:
            messages.error(request, form.errors)
            return redirect('password')

    context = {
        'form':form
    }
    return render(request, 'password.html', context)

def profile(request):
    client = Client.objects.get(user__username = request.user.username)

    context = {
        'client':client
    }

    return render(request, 'profile.html', context)

def gallery(request):
    return render(request, 'gallery.html')

def fitness(request):
    return render(request, 'fitness.html')

def restaurant(request):
    return render(request, 'restaurant.html')

@login_required(login_url='/signin')
def make_reservation(request):
    if request.method == 'POST':
        reservation_num = str(uuid.uuid4())
        adults = int(request.POST['adults'])
        kids = int(request.POST['kids'])
        vol = int(request.POST['quantity'])
        check_in = request.POST['check_in']
        check_out = request.POST['check_out']
        rid = request.POST['itemid']
        item = Room.objects.get(pk=rid)
        bookings = Booking.objects.filter(user__username= request.user.username, paid_order=False)
        if bookings:
            reservation = Booking.objects.filter(user__username=request.user.username, room_id=item.id).first()
            if reservation:
                reservation.quantity += vol
                reservation.check_in = check_in
                reservation.check_out = check_out
                reservation.adults = adults
                reservation.kids = kids
                if reservation.check_in > check_out or reservation.check_out < check_in:
                    reservation.save()
                    messages.success(request, "The room you requested has been added to your Bookings.")
                    return redirect('rooms') 
                else:
                    messages.info(request, "This room is not available for the dates you requested!")
                    return redirect('rooms')
            else:
                newroom = Booking()
                newroom.user = request.user
                newroom.room = item
                newroom.reservation_no = bookings[0].reservation_no
                newroom.room = vol
                newroom.check_in = check_in
                newroom.check_out = check_out
                newroom.adults = adults
                newroom.kids = kids
                newroom.paid_order = False
                newroom.save()
                messages.success(request, 'This Room has been added to your Bookings.')
        else:
            newreservation = Booking() 
            newreservation.user = request.user
            newreservation.room = item
            newreservation.reservation_no = reservation_num
            newreservation.quantity = vol
            newreservation.check_in = check_in
            newreservation.check_out = check_out
            newreservation.adults = adults
            newreservation.kids = kids
            newreservation.paid_order = False
            newreservation.save()
            messages.success(request, 'This Room has been added to your Bookings.')

    return redirect('rooms')  

def my_bookings(request):
    bookings = Booking.objects.filter(user__username=request.user.username, paid_order=False)

    
    for item in bookings:
        d = (item.check_out - item.check_in).days 
        item.nights = d 
        o = item.adults + item.kids
        item.occupants = o
        item.save()


    subtotal = 0
    vat = 0
    total = 0

    for item in bookings:
        subtotal += item.room.price * item.nights * item.quantity

    vat = 0.075 * subtotal

    total = subtotal + vat

    context = {
        'bookings':bookings,
        'subtotal':subtotal,
        'vat':vat,
        'total':total

    }
    return render(request, 'my_bookings.html', context)

def delete_booking(request):
    itemid = request.POST['itemid']
    Booking.objects.filter(pk=itemid).delete()
    messages.success(request, 'Booking deleted.')
    return redirect('mybookings')

def finish_booking(request):
    bookings = Booking.objects.filter(user__username=request.user.username, paid_order=False)
    user = Client.objects.get(user__username=request.user.username)

        
    for item in bookings:
        d = (item.check_out - item.check_in).days 
        item.nights = d
        o = item.adults + item.kids
        item.occupants = o
        item.save()


    subtotal = 0
    vat = 0
    total = 0

    for item in bookings:
        subtotal += item.room.price * item.nights * item.quantity

    vat = 0.075 * subtotal

    total = subtotal + vat

    context = {
        'bookings':bookings,
        'total':total,
        'vat':vat,
        'user':user,
    }
    return render(request, 'finish.html', context)

def make_payment(request):
    if request.method == 'POST':
        api_key = 'sk_test_55b070a7d173af2650b566ef4a1dc7194460ce5f'
        curl = 'https://api.paystack.co/transaction/initialize'
        cburl = 'http://18.222.252.212/completed/'
        total = float(request.POST['total']) * 100
        bookings_code = request.POST['bookings_code']
        pay_code = str(uuid.uuid4())
        user = User.objects.get(username=request.user.username)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']


        # collect data that you will send to paystack
        headers = {'Authorization': f'Bearer {api_key}'}
        data = {'reference':pay_code, 'email':user.email, 'amount': int(total), 'callback_url':cburl, 'order_number':bookings_code}

        # make a call to paystack
        try:
            r= requests.post(curl, headers=headers, json=data)
        except Exception:
            messages.error(request, 'An error occured, please try again')
        else:
            transback = json.loads(r.text)
            rd_url = transback['data']['authorization_url']

            paid = Payment()
            paid.user = user 
            paid.amount = total 
            paid.reservation_no = bookings_code
            paid.pay_code = pay_code
            paid.paid_order = True 
            paid.first_name = first_name
            paid.last_name = last_name
            paid.phone = phone 
            paid.save()

            return redirect(rd_url)        
    return redirect('finish')

def booking_completed(request):
    client = Client.objects.get(user__username=request.user.username)
    rez = Booking.objects.filter(user__username=request.user.username, paid_order=False)

    for item in rez:
        item.paid_order = True
        item.save()

    for item in rez:
        item.paid_order = True
        item.save()

        availability = Room.objects.get(pk=item.room.id)
        availability.max_quantity -= item.quantity
        availability.available = False
        availability.save()

    
    context = {
        'client':client
    }
    
    return render(request, 'completed.html', context)

def history(request):
    profile = Booking.objects.filter(user__username=request.user.username, paid_order= True)

    for item in profile:
        d = (item.check_out - item.check_in).days
        item.nights = d
        o = item.adults + item.kids
        item.occupants = o
        item.save()


    subtotal = 0
    vat = 0
    total = 0

    for item in profile:
        subtotal += item.room.price * item.nights

    vat = 0.075 * subtotal

    total = subtotal + vat

    context={
        'profile':profile,
        'total':total,
        'vat':vat
    }

    return render(request, 'history.html', context)

def delete_history(request):
    itemid = request.POST['itemid']
    Booking.objects.filter(pk=itemid).delete()
    messages.success(request, 'Deleted.')
    return redirect('profile')

def booked(request,id):
    booked = Room.objects.get(pk=id)

    context={
        'booked':booked
    }

    return render(request, 'booked.html', context)

