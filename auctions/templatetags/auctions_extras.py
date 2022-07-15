from django import template
from auctions.models import Listing

register = template.Library()

@register.simple_tag
def get_Listing_list():
    return Listing.objects.all()

