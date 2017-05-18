from __future__ import unicode_literals
import re

from django.db import models

import bcrypt
from django.db import IntegrityError

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def user_validation(self,name,username, email,password,confirm):
        errors = []
        if len(name)<2:
            errors.append("Name must contain more than 2 characters")
        if len(username)<2:
            errors.append("Username must contain more than 2 characters")
        if not email_regex.match(email):
            errors.append('Invalid Email')
        if User.objects.filter(email=email):
            errors.append("Email in use!")
        if len(password)<5:
            errors.append('password too weak')
        if password != confirm:
            errors.append("Passwords do not match")
        return errors

    def create_user(self, name,username, email, password):
        errors=[]
        try:
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            user = User.objects.create(first_name=name, user_name=username, email=email, password=hashed)
            return user
        except IntegrityError:
            errors.append("This User already Exists")
        return errors

    def authenticate_user(self, username, password, request):
        try:
            user = User.objects.get(user_name=username)
            request.session['id'] = user.id
            return bcrypt.hashpw(password.encode(), user.password.encode()) == user.password
        except:
            return False

class BookManager(models.Manager):
    def add_book(self, title, author):
        errors = []
        if len(title)<0:
            errors.append("Must add Title")
        if len(author)<0:
            errors.append("Must add Author")
        else:
            mybook = Book.objects.create(title=title,author=author)
            return mybook
        return errors

class CommentManager(models.Manager):
    def add_comments(self,comment,rating,book,user):
        errors=[]
        if len(comment)<0:
            errors.append("Please add comment")
            return errors
        else:
            Comment.objects.create(comment=comment,rating=rating,user=user, book=book)

class User(models.Model):
    first_name = models.CharField(max_length=225)
    user_name = models.CharField(max_length=225, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=45)
    author = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BookManager()

class Comment(models.Model):
    comment = models.CharField(max_length=250)
    rating = models.CharField(max_length=3)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User, related_name='user_comment')
    book = models.ForeignKey(Book, related_name='book_comment')
    objects = CommentManager()
