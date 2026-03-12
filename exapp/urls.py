from django.urls import path
from .views import *

urlpatterns = [
    path('', expense_list, name='home'),
    path('delete/<int:pk>/', delete_expense, name='delete-expense'),
]
