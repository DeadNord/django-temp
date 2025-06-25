from django.urls import path
from .views import PingView, ItemListCreateView

urlpatterns = [
    path("ping/", PingView.as_view(), name="ping"),
    path("items/", ItemListCreateView.as_view(), name="items"),
]

