from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User

from .models import Transaction
from .utils import makeTx
from hidden import getMyAddress
# Create your views here.

def showIndex(request):
    '''Render main page'''

    txs = Transaction.objects.all().order_by('-created')
    
    if request.method == 'POST':

        # Create and send a transaction then get response
        # and make a Transaction class instance out of it
        response = makeTx()
        recipientAddress = response[0]
        tx_id = response[1]['result']

        Transaction.objects.create(
            id=tx_id, 
            amount=1, 
            sender=getMyAddress(), 
            recipient=recipientAddress)

        return redirect('index')

    context = {'txs': txs}
    return render(request, 'index.html', context)

def loginPage(request):
    '''Login functionality'''

    # If user is already logged in then redirect to the main page
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
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

@staff_member_required(login_url='login')
def showTx(request, pk):

    tx = Transaction.objects.get(id=pk)

    if request.method == 'POST' and request.POST.get('description'):
        tx.description = request.POST.get('description')
        tx.save()

    context = {'tx': tx}

    return render(request, 'singleTx.html', context)
