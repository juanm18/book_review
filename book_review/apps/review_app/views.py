from django.shortcuts import render,redirect,reverse
from models import *
from django.db.models import Q
from django.contrib import messages
from django.db.models import Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# Create your views here.
def index(request):
    return render(request, "index.html")


def register(request):
    name = request.POST['first_name']
    email = request.POST['email']
    username = request.POST['username']
    password = request.POST['password']
    confirm = request.POST['conf_pass']
    errors = []
    errors = User.objects.user_validation(name,  username, email, password, confirm)

    if len(errors)==0:
        user = User.objects.create_user(name, username, email, password)
        request.session['id'] = user.id
        request.session['username'] = username
        request.session['first_name'] = name
        request.session['email'] = email
        return redirect('Books:home')
    for e in errors:
        messages.add_message(request, messages.ERROR, e)
    return redirect('Books:index')

def Login(request):
    username = request.POST['username']
    password = request.POST['password']

    if User.objects.authenticate_user(username, password, request):
        request.session['username']= username
        return redirect('Books:home')
    else:
        messages.add_message(request, messages.ERROR, 'invalid login')
        return redirect('Books:index')

def home(request):
    recent = Comment.objects.order_by("-created_at")[0:3]
    allbooks = Book.objects.all()
    count = Book.objects.count()
    Book.objects.order_by('created_at')

    search_result = Book.objects.all()
    query = request.GET.get("q")
    if query:
        search_result = search_result.filter(
        Q(title__icontains=query)|
        Q(author__icontains=query)
        ).distinct()
    paginator = Paginator(search_result,2)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    return render(request, "home.html", {'recent':recent, 'allbooks':allbooks, 'count':count, 'search_result':search_result, 'page_request_var': page_request_var})

def add(request):
    return render(request, "addbook.html")

def proccess(request):
    title = request.POST['title']
    author = request.POST['author']
    comment = request.POST['reviews']
    rating = request.POST['rating']
    user = User.objects.get(id=request.session['id'])
    errors = []
    if len(errors)==0:
        book = Book.objects.add_book(title,author)
    if len(errors)==0:
        comment = Comment.objects.add_comments(comment,rating,book,user)
    return redirect('Books:home')

def user(request,id):
    user = User.objects.get(pk=id)
    revcount = Comment.objects.filter(user_id=id).count()
    mybooks = Comment.objects.filter(user_id=id)
    return render(request, "user.html",{'user':user, 'revcount':revcount, 'mybooks':mybooks})

def book_info(request,id):
    user = User.objects.get(id=request.session['id'])
    book = Book.objects.get(pk=id)
    comments = Comment.objects.filter(book=book)
    # average = Comment.objects.find(book=book).rating.sum()/rating.count()
    return render(request,"book_info.html",{'book':book,'comments':comments})

def proccess_book(request):
    comment = request.POST['reviews']
    rating = request.POST['rating']
    book_id = request.POST['book_id']
    user = User.objects.get(id=request.session['id'])
    book = Book.objects.get(id = book_id)
    comment = Comment.objects.add_comments(comment,rating,book,user)
    return redirect(reverse('Books:bookinfo', kwargs={'id':book_id}))

def delete(request,id):
    Comment.objects.filter(id=id).delete()
    return redirect('Books:home')

def deletebook(request,id):
    books = Book.objects.filter(id=id)
    books.delete()
    return redirect('Books:home')

def logout(request):
    request.session.clear()
    return redirect('/')




# def get_query(self):
#     result =
