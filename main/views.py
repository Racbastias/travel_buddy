from django.contrib import messages
from django.db.models import Count
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required
from main.models import User, Travel, Traveler

def index(request):
    return redirect('/register')

@login_required
def travels(request): # display the dashboard
    user = request.session['user']
    userid = request.session['user']['id']
    creator = User.objects.get(id=userid)
    traveler = Traveler.objects.get(id=userid)
    mytravels = Travel.objects.filter(travelers = userid).order_by('-created_at')
    othertravels = Travel.objects.all().order_by('-created_at').exclude(creator_id = userid)
    
    context = {
        "user": user,
        "creator": creator,
        "traveler": traveler,
        "mytravels": mytravels,
        "othertravels": othertravels,
    }
    return render(request, 'main.html', context)
    
@login_required
def join(request, id): # add a user to a trip like traveler
    user = request.session['user']
    userid = request.session['user']['id']
    traveler = Traveler.objects.get(id=userid)
    travel = Travel.objects.get(id=id)
    
    travel.travelers.add(traveler)
    travel.save()
    
    messages.success(request, f'You have joined to this trip')
    return redirect(f'/travels/destination/{travel.id}')

@login_required
def travels_add(request): #create a new travel from session user
    if request.method == 'GET':
        user = request.session['user']
        context = {
            "user": user,
        }
        return render(request, 'newtravel.html', context)
    
    else:
        user = request.session['user']
        userid = request.session['user']['id']
        traveler = Traveler.objects.get(id=userid)
        destination = request.POST['destination']
        description = request.POST['description']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        
        errors = Travel.objects.basicvalidator(request.POST)
        if len(errors) > 0:
            for key, mensaje_de_error in errors.items():
                messages.error(request, mensaje_de_error)
            return redirect('/travels/add')
        
        newtravel = Travel.objects.create(
            destination = destination,
            description = description, 
            start_date = start_date,
            end_date = end_date,
            creator_id = userid,
        )
        newtravel.travelers.add(traveler)
        newtravel.save()
        
        messages.success(request, f'You have added a new Trip!')
        return redirect(f'/travels')

@login_required
def travels_id(request, id): # show the travel information
    user = request.session['user']
    userid = request.session['user']['id']
    travel = Travel.objects.get(id=id)
    creatorid = travel.creator.id
    owntravel = Traveler.objects.get(id=creatorid)
    travelid = travel.id
    travelers = Traveler.objects.all().filter(travels = travelid).exclude(id = creatorid)
    
    context = {
        "user": user,
        "userid": userid,
        "travel": travel,
        "travelers": travelers,
    }
    return render(request, 'travels.html', context)

@login_required
def delete_id(request, id): # delete a user travel
    user = request.session['user']
    userid = request.session['user']['id']
    travel = Travel.objects.get(id=id)
    creator = travel.creator_id
    context = {
        "creator": creator
    }
    if creator == userid:
        travel.delete()
        messages.error(request, f'Your trip has been deleted')
        return redirect(f'/travels', context)
    
    else:
        messages.error(request, f'You are not allowed to delete this')
        return redirect(f'/travels', context)

@login_required
def cancel_id(request, id): # exit from an added travel
    user = request.session['user']
    userid = request.session['user']['id']
    travel = Travel.objects.get(id=id)
    traveler = Traveler.objects.get(id=userid)
    context = {
        "traveler": traveler
    }
    if travel.creator_id == userid:
        travel.delete()
        messages.error(request, f'Your trip has been deleted')
        return redirect(f'/travels', context)
    
    else:
        travel.travelers.remove(traveler)
        travel.save()
    
    messages.error(request, f'You cancel this journey')
    return redirect(f'/travels', context)