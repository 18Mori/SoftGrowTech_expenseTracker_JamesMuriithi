from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    TYPES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Rent', 'Rent'),
        ('Transport', 'Transport'),
        ('Entertainment', 'Entertainment'),
        ('Utilities', 'Utilities'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    transaction_type = models.CharField(max_length=10, choices=TYPES, null=True)
    date = models.DateField(auto_now_add=True)

    CATEGORY_STYLES = {
        'Food': 'bg-blue-100 text-blue-800',
        'Utilities': 'bg-green-100 text-green-800',
        'Entertainment': 'bg-yellow-100 text-yellow-800',
        'Rent': 'bg-purple-100 text-purple-800',
        'Transport': 'bg-red-100 text-red-800',
    }

    @property
    def category_color_class(self):
        return self.CATEGORY_STYLES.get(self.category, 'bg-gray-100 text-gray-800')

    def __str__(self):
        return f"{self.title} - {self.amount}"