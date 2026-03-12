from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .serializers import *
from django.db.models import Sum

def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    total_balance = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    if request.method == "POST":
        serializer = ExpenseSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return redirect('home')
      
    return render(request, 'Home.html', {
        'expenses': expenses,
        'total_balance': total_balance
    })
    
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, id=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
    return redirect('home')
    