from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .serializers import *
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages



def expense_list(request):
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    
    daily_total = expenses.filter(date=today).aggregate(Sum('amount'))['amount__sum'] or 0
    weekly_total = expenses.filter(date__gte=week_start).aggregate(Sum('amount'))['amount__sum'] or 0
    monthly_total = expenses.filter(date__gte=month_start).aggregate(Sum('amount'))['amount__sum'] or 0
    
    if request.method == "POST":
        serializer = ExpenseSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save(user=request.user)
            messages.success(request, 'Added successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Error!! Plese check the form & try again.')
    
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
        messages.warning(request, "Deleted.")
    return redirect('home')
    