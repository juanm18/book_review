from django.conf.urls import url, include
from views import *

urlpatterns = [

    url(r'^$', index, name='index'),
    url(r'^authenticate$', Login, name='login'),
    url(r'^register$',register, name='register'),
    url(r'^home$', home, name='home'),
    url(r'^add$', add, name='add'),
    url(r'^proccess$', proccess, name='proccess'),
    url(r'^proccess_book$', proccess_book, name='proccessbook'),
    url(r'^book/(?P<id>\d+)$', book_info,name='bookinfo'),
    url(r'^user/(?P<id>\d+)$', user, name='user'),
    url(r'^book/delete/(?P<id>\d+)$', delete, name='delete'),
    url(r'^delete/(?P<id>\d+)$',deletebook, name='deletebook'),
    url(r'^logout$', logout,name='logout'),



]
