
from django.contrib import admin
from django.urls import path, re_path
from django.urls import include
from config import settings
from menu.views import MenuDetailView, MenuItemListView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('<slug:slug>/', MenuDetailView.as_view(), name='first_level'),
    path('<slug:parent>/<slug:url>/', MenuItemListView.as_view(), name='second_level'),
    path('<slug:parent>/<slug:url1>/<slug:url2>/', MenuItemListView.as_view(), name='third_level'),
    path('<slug:parent>/<slug:url1>/<slug:url2>/<slug:url3>/', MenuItemListView.as_view(), name='fourth_level'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
