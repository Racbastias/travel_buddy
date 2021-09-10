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
def travels(request):
    if request.method == 'GET':
        user = request.session['user']
        userid = request.session['user']['id']
        traveler = User.objects.get(id=userid)
        usertravels = Travel.objects.filter(travelinfo_id = userid)
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
    
    else:
        travelid = request.POST['travelid']
        travelerid = request.session['user']['id']

        messages.success(request, f'You have joined to this trip')
        return redirect(f'/travels/destination/{travelid}')

@login_required
def travels_add(request):
    if request.method == 'GET':
        user = request.session['user']
        context = {
            "user": user,
        }
        return render(request, 'newtravel.html', context)
    
    else:
        user = request.session['user']
        userid = request.session['user']['id']
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
        
        messages.success(request, f'You have added a new Trip!')
        return redirect(f'/travels/destinationid/{id}')

@login_required
def travels_id(request, id):
    
    book = Book.objects.get(id=id)
    bookid = book.id
    user = request.session['user']
    userid = request.session['user']['id']
    reviews = Review.objects.filter(book_id = book.id).order_by('-created_at')
    book_reviews = book.reviews.all()
    book_ids = []
    for book in book_reviews:
        book_ids.append(book.user_id)
        
    context = {
        "user": user,
        "userid": userid,
        "book": book,
        "bookid": bookid,
        "reviews": reviews,
        "book_ids": book_ids,
    }
    return render(request, 'travels.html', context)

@login_required
def delete_id(request, id):
    user = request.session['user']
    userid = request.session['user']['id']
    review = Review.objects.get(id=id)
    insidebook_id = review.book_id
    context = {
        "insidebook_id": insidebook_id
    }
    if review.user_id == userid:
        review.delete()
        messages.error(request, f'Your review has been deleted')
        return redirect(f'/books', context)
    
    else:
        messages.error(request, f'You are not allowed to delete this')
        return redirect(f'/books', context)