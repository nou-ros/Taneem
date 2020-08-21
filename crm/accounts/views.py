from django.shortcuts import render, redirect
from django.http import HttpResponse
# for creating multiple forms within one form
from django.forms import inlineformset_factory
# for django authentication
from django.contrib.auth import authenticate, login, logout
# for flash messages
from django.contrib import messages

# to restrict accessing pages without logging in
from django.contrib.auth.decorators import login_required


#custom authentication decorator 
#custom allowed pages decorator
from .decorators import unauthenticated_user, allowed_users, admin_only

from .models import *

from .forms import OrderForm, CreateUserForm, CustomerForm

from .filters import OrderFilter    

# Create your views here.

#used custom authentication decorators
@unauthenticated_user
def registerPage(request):
    # we used this to test the django usercreationform
    # form = UserCreationForm()
    form = CreateUserForm()
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            #signals is working here....
            # used the customer profile signal here
            messages.success(request, 'Account has been created for ' + username)
            return redirect('login')

    context = {
        'form':form
    }

    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # authenticating the information 
        user = authenticate(request, username=username, password=password)

        # checking user information availability
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Username or Password incorrect')

    context = {}

    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def about(request):
    context = {}

    return render(request, 'accounts/about.html', context)

def contact(request):
    context = {}

    return render(request, 'accounts/contact.html', context)

# login decorator by django
@login_required(login_url='login')
@admin_only
# we can send multiple roles in decorator
# @allowed_users(allowed_roles=['admin', 'staff'])
def dashboard(request):
    orders = Order.objects.all().order_by('-date_created')
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'orders':orders,
        'customers': customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,

    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    # fetching all the orders of the customer
    orders = request.user.customer.order_set.all().order_by('-date_created')

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'orders':orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
    }
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    
    if request.method == 'POST':
        # request files is used as we are saving images also 
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'accounts/account_settings.html', context)

@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    context = {
        'products':products
    }
    return render(request, 'accounts/products.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    # getting all the orders of the selected customer
    orders = customer.order_set.all()
    order_count = orders.count()

    # searching
    # filtering from all the ordered items
    search = OrderFilter(request.GET, queryset=orders)
    orders = search.qs

    context = {
        'customer': customer, 
        'orders': orders, 
        'order_count': order_count,
        'search': search
    }
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
# to views all ordered items
def orders(request):
    orders = Order.objects.all().order_by('-date_created')
    
    context = {
        'orders': orders
    }
    return render(request, 'accounts/orders.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
# to views all ordered items
def allCustomers(request):
    customers = Customer.objects.all().order_by('-date_created')
    
    context = {
        'customers': customers
    }
    return render(request, 'accounts/all_customer.html', context)

@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    # parent model then child model 
    # extra is the number of multiple form input
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=2)
    customer = Customer.objects.get(id=pk)
    
    # form = OrderForm(initial={'customer':customer})
    #queryset=Order.objects.none() this will help not to render the already existing ordered products
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':
        # print("printing Post: ", request.POST)
        #sending the data in the form
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {
        # 'form':form
        'form': formset
    }
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    # prefilling the update form 
    form = OrderForm(instance=order)
    # saving the updated data
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form':form
    }
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    # getting the order with the pk
    order_item = Order.objects.get(id=pk)

    # deleting the order
    if request.method == "POST":
        order_item.delete()
        return redirect('/')

    context = {
        'order_item': order_item
    }
    return render(request, 'accounts/delete.html', context)
