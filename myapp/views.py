from django.shortcuts import render,HttpResponse,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from . models import Car, Location
from django.http import HttpResponseNotFound

# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    return render (request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confirm password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

def index(request):
    return render(request ,'index.html')

def car_detail_by_make(request, make):
    try:
        car = Car.objects.get(make=make)
        return render(request, 'car.html', {'car': car})
    except Car.DoesNotExist:
        return HttpResponseNotFound("Car with make '{}' does not exist.".format(make))
    
def car_detail(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    return render(request, 'car.html', {'car': car})
    
    
def searching(request):
    query = request.GET.get('search')
    destination = request.GET.get('destination')
    # start_date = request.GET.get('start_date')
    # start_datetime = request.GET.get('start_datetime')
    # end_date = request.GET.get('end_date')
    # end_datetime = request.GET.get('end_datetime')

    results = Car.objects.all()
    if query:
        results = results.filter(locations__city__icontains=query)


    return render(request, 'search.html', {'results': results, 'query': query, 'destination': destination})

    # return HttpResponse('this is search page')