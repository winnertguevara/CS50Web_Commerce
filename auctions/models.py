from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.CharField(max_length=50)
    category = models.CharField(max_length=20, blank=True)
    image = models.ImageField(null=True, upload_to='media', blank= True)
    listedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listedBy')
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null = True, related_name='winner')
    watchlist = models.ManyToManyField(User)

    def save(self):
        self.title = (self.title).capitalize()
        self.description = (self.description).capitalize()
        self.category = (self.category).capitalize()
        return super(Listing, self).save()
        
    def __str__(self):
        return (str(self.title))

class Bid(models.Model):
    bid = models.DecimalField(max_digits=20, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    
    class Meta():
        ordering = ('-bid',)
    
    def __str__(self):
        return (str(self.id))

class Comment(models.Model):
    comment = models.CharField(max_length = 200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    
    def __str__(self):
        return (str(self.id))
