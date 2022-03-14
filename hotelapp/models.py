from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media', default='pix.jpg')

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'category'
        managed = True
        verbose_name = 'category'
        verbose_name_plural = 'categories'

class Room(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media', default='pix.jpg')
    description = models.TextField()
    available = models.BooleanField(default=True)
    price = models.FloatField(default=True)
    max_quantity = models.IntegerField(default=1)
    min_occupants = models.IntegerField(default=1)
    max_occupants = models.IntegerField(default=1)
    min_adults = models.IntegerField(default=1)
    max_adults = models.IntegerField(default=1)
    min_kids = models.IntegerField(default=1)
    max_kids = models.IntegerField(default=1)



    def __str__(self):
        return self.name
    

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    reservation_no = models.CharField(max_length=50)
    paid_order = models.BooleanField()
    check_in = models.DateField(default=1)
    check_out = models.DateField(default=1)
    adults = models.IntegerField(default=1)
    kids = models.IntegerField(default=1)


    def __str__(self):
        return self.user.username

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    reservation_no = models.CharField(max_length=36)
    pay_code = models.CharField(max_length=36)
    paid_order = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
    


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    
    def __str__(self):
        return self.user.username