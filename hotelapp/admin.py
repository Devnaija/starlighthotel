from django.contrib import admin
from . models import Category, Room, Booking, Payment, Client


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image')

class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'image', 'description', 'available', 'price', 'max_quantity', 'min_occupants', 'max_occupants', 'min_adults', 'max_adults', 'min_kids', 'max_kids' )    

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'reservation_no', 'check_in', 'check_out','quantity', 'adults','kids', 'paid_order',)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'reservation_no', 'pay_code', 'paid_order', 'first_name', 'last_name', 'phone' )

class ClientAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name','last_name','phone']



admin.site.register(Category,CategoryAdmin)
admin.site.register(Room,RoomAdmin)
admin.site.register(Booking,BookingAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(Client,ClientAdmin)
