from .models import *
def menu_links(request):
    links=categories.objects.all()
    return dict(links=links)