from django.contrib.auth.models import User
from django.db import models


class cat(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class AddItemAdmin(models.Model):
    category = models.ForeignKey(cat, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="myimage")
    productName = models.CharField(max_length=100)
    productPrice = models.IntegerField()
    productDescription = models.TextField()
    def __str__(self):
        return self.productName



class book_table(models.Model):
    name=models.CharField(max_length=50)
    phone_no=models.IntegerField()
    email=models.EmailField()
    person=models.IntegerField()
    date=models.DateField()
    random_string=models.CharField(max_length=6)
    def __str__(self):
        return self.name


class Reg(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=0)
    image = models.FileField(upload_to='myimage',default="profile.png")
    otp = models.CharField(max_length=10,null=True)
    contact = models.IntegerField(null=True)

















