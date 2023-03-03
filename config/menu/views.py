
from django.views.generic.detail import DetailView
from .models import MenuItem, Menu
from django.views import generic


class MenuDetailView(DetailView):
    model = Menu
    template_name = 'index.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class MenuItemListView(generic.ListView):
    model = MenuItem
    template_name = 'index.html'
