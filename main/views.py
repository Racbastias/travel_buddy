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
    traveler = Traveler.objects.get(id=userid)
    usertravels = Travel.objects.filter(travelers = traveler.id)
    travelers = Traveler.objects.all()
    travels = Travel.objects.all().order_by('-created_at').exclude(travelinfo_id = userid)
    context = {
        "user": user,
        "traveler": traveler,
        "usertravels": usertravels,
        "travelers": travelers,
        "travels": travels,
    }
    return render(request, 'main.html', context)
    
@login_required
def join(request, id): # add a user to a trip like traveler
    user = request.session['user']
    userid = request.session['user']['id']
    thistravel = Travel.objects.get(id = id)
    
    traveler = Traveler.objects.create(
        infotraveler_id = userid,
        travels_id = thistravel.id
    )
    
    thistravel.travelers.add(traveler)
    thistravel.save()
    
    messages.success(request, f'You have joined to this trip')
    return redirect(f'/travels/destination/{thistravel.id}')

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
        
        newtravel = Travel.objects.create(
            destination = destination,
            description = description, 
            start_date = start_date,
            end_date = end_date,
            travelinfo_id = userid
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
    travelcreatorid = travel.travelinfo.id
    travelid = travel.id
    travelers = Travel.objects.all().exclude(travelinfo_id = travelcreatorid)
    
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
    travelinfo_id = travel.travelinfo_id
    context = {
        "travelinfo_id": travelinfo_id
    }
    if travel.travelinfo_id == userid:
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
    travelinfo_id = travel.travelinfo_id
    context = {
        "travelinfo_id": travelinfo_id
    }
    if travel.travelinfo_id == userid:
        travel.delete()
        messages.error(request, f'Your trip has been deleted')
        return redirect(f'/travels', context)
    
    else:
        messages.error(request, f'You are not allowed to delete this')
        return redirect(f'/travels', context)