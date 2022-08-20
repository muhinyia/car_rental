from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from company.models import Car, Reservation, Station


def register(request):
    if request.method == 'POST':
        # Get form Values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        id_number = request.POST['id']
        email = request.POST['email']

        # check username
        username = email
        password = id_number
        if User.objects.filter(username=username).exists():
            messages.error(request, 'This Email Exists!!')
            return redirect('register')
        else:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email Exists!!!')
                return redirect('register')
            else:
                # adding user since all the validation passed
                user = User.objects.create_user(username=username, password=password, email=email,
                                                first_name=first_name, last_name=last_name)
                # Login after register
                # auth.login(request, user)
                # messages.SUCCESS(request,'You are now logged in')
                # retun redirect('index')
                user.save()
                messages.success(
                    request, 'You Have Registered Successfully')
                return redirect('login')

    else:
        return render(request, 'accounts/register.html', )


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:

            auth.login(request, user)

            messages.success(request, 'You are Logged in Welcome ')
            if username == 'admin':
                return redirect('admins')

            else:

                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    return render(request, 'accounts/login.html', )


@login_required
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are Logged out')

    return redirect('login')


@login_required
def dashboard(request):
    user_id = request.user.id
    this_user = get_object_or_404(User, pk=user_id)
    reservations = Reservation.objects.all().filter(
        customer=this_user, has_returned=False)
    context = {'reservations': reservations, }
    username = request.user.username
    if username == 'admin':
        return redirect('admins')

    return render(request, 'accounts/dashboard.html', context)
