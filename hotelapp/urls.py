from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.categories, name='categories'),
    path('category/<str:id>/', views.single_category, name='categoryroom'),
    path('rooms/', views.rooms, name='rooms'),
    path('details/<str:id>/', views.single_room, name='details'),
    path('gallery/', views.gallery, name='gallery'),
    path('fitness/', views.fitness, name='fitness'),
    path('restaurant/', views.restaurant, name='restaurant'),
    path('signin/', views.loginform, name='signin'),
    path('logout/', views.logoutt, name='logout'),
    path('signup/', views.signupform, name='signup'),
    path('password/', views.password, name='password'),
    path('makereservation/', views.make_reservation, name='makereservation'),
    path('mybookings/', views.my_bookings, name='mybookings'),
    path('deletebooking/', views.delete_booking, name='deletebooking'),
    path('deletehistory/', views.delete_history, name='deletehistory'),
    path('makepayment/', views.make_payment, name='makepayment'),
    path('finish/', views.finish_booking, name='finish'), 
    path('completed/', views.booking_completed, name='completed'),
    path('booked/<str:id>/', views.booked, name='booked'),
    path('history/', views.history, name='history'),
    path('profile/', views.profile, name='profile'),
]
