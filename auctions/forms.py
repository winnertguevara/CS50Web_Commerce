from django import forms
from django.forms import TextInput, Textarea, NumberInput
from .models import *

class ListingForm (forms.ModelForm):
    
    class Meta:
        model = Listing
        exclude = ['listedBy', 'watchlist','active', 'winner']
        widgets = {
            'title': forms.TextInput(attrs={'autofocus': True, 'class': 'form-control','placeholder':'Title'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Price'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Description'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Category'})
        }

class BidForm (forms.ModelForm):
    
    class Meta:
        model = Bid
        fields = ('bid',)
        widgets = {
            'bid': forms.NumberInput(attrs={'class': 'form-control',
                                          'placeholder': 'Enter your bid'}),
        }
        
class CommentForm (forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('comment',)
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control rounded-0',
                                             'placeholder': 'Enter your comment',
                                             'rows': 3
                                          }),
        }
