
from django.contrib.auth.decorators import login_required
from myapp.models import *
from .models import *
from django.shortcuts import render,redirect
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages



# everytghing related to users
# login view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser : # important for the redirection either the admin or the member access
                login(request, user)
                return redirect('admin')
            elif user.is_verified : # the user has to be verified by an admin
                login(request, user)
                return redirect('member')
            else:
                return render(request, 'user/login.html', {'form': form, 'error': "Votre compte n'a pas encore été validé par nos éqiuipes"})
        else:
            return render(request, 'user/login.html', {'form': form, 'error': 'Identifiants incorrects'})
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})

@login_required 
def verify_user(request, user_id): # just the button to toggle on the admin page
    user = get_object_or_404(User, id=user_id)
    user.is_verified = True
    user.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))



@login_required
def admin(request):
    userss=User.objects.all()
    context={
        'users':userss,
    }
    return render(request,"admin/user.html",context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

def register_view(request):
    if request.method == 'POST':
        print('form valid')
        form = RegisterForm(request.POST, request.FILES)
        print('The files collected : ',request.FILES)
        if form.is_valid(): # the form was invalid because of the errors but i missed it parceque je pensais que c'etait en relation avec les files
            print('Im saving the file ')
            form.save()
            return redirect('login')
        else:
            print('Form is not valid')
            print(form.errors) # super important to display the erorrs related to the form 
            form.errors
    else:
        print('actualy im in the else')
        form = RegisterForm()
    return render(request, 'user/register.html', {'form': form})










# everything related to les bijoux

@login_required
def product(request):
    product=Product.objects.all()
    context={
        'products':product,
    }
    return render(request,"admin/products.html",context)


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product')
    else:
        form = ProductForm()
    return render(request, 'admin/product_create.html', {'form': form, 'title': 'Ajouter un produit'})

@login_required
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin/product_update.html', {'form': form, 'title': 'Modifier le produit'})

@login_required
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('product')

@login_required 
def available(request, product_id): # same logic as the verify_user
    product = get_object_or_404(Product, id=product_id)
    product.availbale= True
    product.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))



