from rest_framework import serializers
from .models import *

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'title', 'amount', 'category', 'transaction_type', 'date']