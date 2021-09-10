from django.contrib import messages
from django.shortcuts import redirect, render
from django.db import IntegrityError
import bcrypt
from main.models import User
from .decorators import login_required


@login_required
def logout(request):
    del request.session['user']
    return redirect('/register')

def login(request):
    if request.method == "GET":
        return render(request, 'register.html')
        
    else:
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            user = User.objects.get(email=email)
        
        except User.DoesNotExist:
            messages.error(request, 'User or password does not exist')
            return redirect('/register')
        
        if  not bcrypt.checkpw(password.encode(), user.password.encode()): 
            messages.error(request, 'User or password does not exist')
            return redirect('/register')
        
        request.session['user'] = {
            'id': user.id,
            'name': user.name,
            'nickname': user.nickname,
            'email': user.email,
            'avatar': user.avatar
        }
        messages.success(request, f'Welcome {user.nickname}')
        return redirect('/books')

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    
    else:
    
        name = request.POST['name']
        nickname = request.POST['nickname']
        email = request.POST['email']
        avatar = request.POST['gender']
        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        password_confirm = request.POST['password_confirm']

        errors = User.objects.basicvalidator(request.POST)
        if len(errors) > 0:
            for key, mensaje_de_error in errors.items():
                messages.error(request, mensaje_de_error)
            return redirect('/register')
        try: 
            user = User.objects.create(
                name = name,
                nickname = nickname,
                email = email,
                password = password,
                avatar = avatar
            )
        except IntegrityError:
            messages.error(request, 'This Email already exist')
            return redirect('/register')
            
        request.session['user'] ={
            'id': user.id,
            'name': user.name,
            'nickname': user.nickname,
            'email': user.email,
            'avatar': avatar
        }
        messages.success(request, 'New user has been created')
        return redirect('/books')
