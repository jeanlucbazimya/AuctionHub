from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.auct_list, name="auct_list"),
    path("product/<int:id>", views.product, name="product"),
    path("comment/<int:id>",views.comment, name="comment"),
    path("watch", views.watch, name="watch"),
    path("status", views.status, name="status"),
    path("mine", views.mine, name="mine"),
    path("category", views.categories, name="category"),
    path("list/<str:category>", views.categories_list, name="list"),
    path("remove_watch", views.remove_watch, name="remove_watch")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)