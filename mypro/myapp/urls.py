from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('index.html/', views.index, name="index_html"),
    path('menu.html/', views.menu, name="menu_html"),
    path('about.html/', views.about, name="about"),
    path('book.html/', views.book, name="book"),
    path('mycoff.html/', views.coff, name="my_coff"),
    path('cart.html/', views.cart, name="cart"),
    path('home.html/', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin', views.signin, name='signin'),
    path('signin/', views.signin, name='signin'),
    path('signin/', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('booktable/', views.booktable, name='booktable'),
    path('booksuccess.html/', views.booksuccess, name='booksuccess'),
    path('otp/', views.otp, name='otp'),
    path('reset/', views.reset, name='reset'),
    path('forget/', views.forget, name='forget')

]