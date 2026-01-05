
from django.urls import path
from . import views

app_name = "credits"
urlpatterns = [
    path("wallet/", views.wallet_view, name="wallet"),
    path("transfer/", views.transfer_view, name="transfer"),
]
