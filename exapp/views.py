from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .serializers import *
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta



def expense_list(request):
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    
    transactions = Expense.objects.filter(user=request.user).order_by('-date')
    
    daily_total = transactions.filter(date=today).aggregate(Sum('amount'))['amount__sum'] or 0
    weekly_total = transactions.filter(date__gte=week_start).aggregate(Sum('amount'))['amount__sum'] or 0
    monthly_total = transactions.filter(date__gte=month_start).aggregate(Sum('amount'))['amount__sum'] or 0
    
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    
    if request.method == "POST":
        serializer = ExpenseSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return redirect('home')
    
    return render(request, 'Home.html', {
        'expenses': expenses,
        'daily_total': daily_total,
        'weekly_total': weekly_total,
        'monthly_total': monthly_total,
    })
    
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, id=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
    return redirect('home')
    