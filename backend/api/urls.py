from django.urls import path
from . import views

urlpatterns = [
    path('status/', views.system_status, name='system_status'),
    path('transfer/', views.transfer_money, name='transfer_money'),
    path('create/', views.create_account, name='create_account'),
    path('update-note/', views.update_note, name='update_note'),
]