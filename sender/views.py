from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

# Create your views here.

def showIndex(request):
    return render(request, 'index.html')

def loginPage(request):

    # If user is already logged in then redirect to the main page
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':

        print(request.POST)
        try:
            username = request.POST['username']
            password = request.POST['password']
        except:
            # Show flash message if username or password weren't written
            print('You entered something wrong. Try again') # WILL BE A FLASH MESSAGE

        # Check if username and password are correct
        try:
            user = User.objects.get(username=username)
        except:
            # Show flash message if profile with this username doesn't exist
            print('Username does not exist') # WILL BE A FLASH MESSAGE

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')

    return render(request, 'loginPage.html')

def logoutPage(request):
    '''Logout user when button pressed.'''

    logout(request)
    return redirect('index')
