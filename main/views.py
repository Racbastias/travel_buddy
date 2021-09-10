from django.contrib import messages
from django.db.models import Count
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required
from main.models import User, Book, Author, Review


def index(request):
    return redirect('/register')

@login_required
def books(request):
    user = request.session['user']
    authors = Author.objects.all()
    books = Book.objects.all().order_by('title')
    reviews = Review.objects.all().order_by('-created_at')[:3]
    context = {
        "user": user,
        "authors": authors,
        "books": books,
        "reviews": reviews,
    }
    return render(request, 'main.html', context)

@login_required
def new_author(request):
    name = request.POST['newauthor']
    
    try: 
        Author.objects.create(name=name)
        
    except IntegrityError:
        messages.error(request, 'This Name already exist')
        return redirect('/books/add')
    
    messages.success(request, f'You have added a new Author')
    return redirect(f'/books/add')
    
@login_required
def add(request):
    if request.method == 'GET':
        user = request.session['user']
        author = Author.objects.all()
        context = {
            "user": user,
            "author": author
        }
        return render(request, 'newbook.html', context)
    
    else:
        user = request.session['user']
        userid = request.session['user']['id']
        reader = User.objects.get(id=userid)
        author = request.POST['author']
        title = request.POST['title']
        review = request.POST['review']
        rating = int(request.POST['rating'])
        
        try: 
            newbook = Book.objects.create(
                title = title,
                author_id = author
            )    
        except IntegrityError:
            messages.error(request, 'This Book already exist')
            return redirect('/books/add')
        
        new_review = Review.objects.create(
            review = review,
            rating = rating,
            user_id = userid,
            book_id = newbook.id
        )
        messages.success(request, f'You have done a new review to {newbook.title}')
        return redirect(f'/books/{newbook.id}')

@login_required
def book_id(request, id):
    if request.method == 'GET':
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
        return render(request, 'book.html', context)
    
    else:
        user = request.session['user']
        userid = request.session['user']['id']
        review = request.POST['review']
        rating = request.POST['rating']
        book = Book.objects.get(id=id)
        Review.objects.create(
            review = review,
            rating = rating,
            user_id = userid,
            book_id = book.id
        )
        messages.success(request, f'You have done a new review to {book.title}')
        return redirect(f'/books/{book.id}')

@login_required
def users_id(request, id):
    user = request.session['user']
    reader = User.objects.get(id=id)
    reviewsuser = Review.objects.filter(user_id = reader.id)
    reviews = []
    for review in reviewsuser:
        reviews.append(review)
    #import pdb; pdb.set_trace()
    context = {
        "user": user,
        "reader": reader,
        "reviewsuser": len(reviews),
        "books": Book.objects.filter(reviews__user_id=reader.id),
    }
    return render(request, 'reader.html', context)

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