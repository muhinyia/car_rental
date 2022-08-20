from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from .models import Car, Station, Reservation, Contact
from django.core.paginator import Paginator
from .counties import counties, towns
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import date
from django.utils.dateparse import parse_date
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash


def index(request):
    cars = Car.objects.order_by('fee').filter(available=True)[:12]

    return render(request, 'pages/index.html', locals())


def display(request):
    cars = Car.objects.order_by('fee').filter(available=True)
    paginator = Paginator(cars, 3)
    page = request.GET.get('page')
    paged_cars = paginator.get_page(page)
    context = {'cars': paged_cars}
    return render(request, 'pages/display.html', context)


def automobile(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    context = {
        'car': car,
        'counties': counties,
        'towns': towns
    }
    return render(request, 'pages/automobile.html', context)


@login_required
def reserve(request):
    if request.method == 'POST':
        user_id = request.user.id
        car_id = request.POST['car_id']
        return_date_ = request.POST['return_date']
        phone = request.POST['phone']
        id_number = request.POST['id_number']
        town = request.POST['town']
        county = request.POST['county']

        return_date = parse_date(return_date_)

        if date.today() > return_date:

            messages.error(
                request, 'Please enter a date greater than today or the date today!!!')
            car = get_object_or_404(Car, pk=car_id)
            context = {
                'car': car,
                'counties': counties,
                'towns': towns
            }
            return render(request, 'pages/automobile.html', context)
        else:
            # logic
            station = get_object_or_404(Station, town=town)
            car = get_object_or_404(Car, pk=car_id)
            user = get_object_or_404(User, pk=user_id)
            has_reserved = Reservation.objects.all().filter(
                customer=user, has_returned=False)
            if has_reserved:
                messages.error(
                    request, 'You already have a pending reservation')
                return redirect('dashboard')

            reservation = Reservation(
                car=car, station=station, id_number=id_number, return_date=return_date, customer=user, customer_phone=phone)
            reservation.save()

            # making this reserved car unavailable
            c = Car.objects.get(pk=car_id)
            c.available = False
            c.save()
            update_session_auth_hash(request, user)

            return render(request, 'pages/book_success.html', locals())
    else:
        return render(request, 'pages/contacts.html')


@login_required
def admins(request):
    reservations = Reservation.objects.filter(has_returned=False)

    context = {'reservations': reservations, }
    return render(request, 'accounts/admins.html', context)


@login_required
def clearing(request):
    if request.method == 'POST':
        customer_id = request.POST['customer_id']
        car = get_object_or_404(
            Reservation, id_number=customer_id, has_returned=False)
        return render(request, 'accounts/reserved_cars.html', {'car': car})

    else:
        reservations = Reservation.objects.filter(has_returned=False)

        context = {'reservations': reservations, }

        return render(request, 'accounts/admins.html', context)


@login_required
def hire_out(request, reserve_id):
    reservation = get_object_or_404(Reservation, pk=reserve_id)
    reservation.has_paid = True
    reservation.save()
    messages.success(
        request, "The car has been hired out to the customer Please Direct Him/Her to the Garage for Collection")
    return redirect('admins')


@login_required
def car_clear(request, reserve_id):
    get_car = get_object_or_404(Reservation, pk=reserve_id)
    that_car = get_car.car

    if get_car.is_overdue == False:
        get_car.has_returned = True
        get_car.save()
        that_car.available = True
        that_car.save()
        messages.success(
            request, "You Successfully Cleared the Customer and the Car Added Back to System For Hire")
        return redirect('admins')
    else:
        messages.error(
            request, "This Customer Needs to first clear the fee and Fine Applied For Delay")
        return redirect('admins')


@login_required
def feedback(request):
    contacts = Contact.objects.all()
    return render(request, 'accounts/contacts.html', locals())


def contact(request):
    if request.method == 'POST':
        customer = request.POST['customer']
        email = request.POST['email']
        message = request.POST['message']

        contacts = Contact(customer=customer, email=email, message=message)
        contacts.save()
        messages.success(
            request, "We Received your message. thankyou for contacting us. We will get back to you shortly")
        return render(request, 'pages/contacts.html')
    else:
        return render(request, 'pages/contacts.html')
