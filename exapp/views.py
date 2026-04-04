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
    
    expenses = Expense.objects.filter(user=request.user)
    
    def get_totals(queryset):
        income = queryset.filter(transaction_type='INCOME').aggregate(Sum('amount'))['amount__sum'] or 0
        expense = queryset.filter(transaction_type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or 0
        return income, expense, (income - expense)
    
    daily_in, daily_out, daily_net = get_totals(expenses.filter(date=today))
    weekly_in, weekly_out, weekly_net = get_totals(expenses.filter(date__gte=week_start))
    monthly_in, monthly_out, monthly_net = get_totals(expenses.filter(date__gte=month_start))
    
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
        'daily_in': daily_in,
        'daily_out': daily_out,
        'daily_net': daily_net,
        'weekly_in': weekly_in,
        'weekly_out': weekly_out,
        'weekly_net': weekly_net,
        'monthly_in': monthly_in,
        'monthly_out': monthly_out,
        'monthly_net': monthly_net,
    })
    
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, id=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.warning(request, "Deleted.")
    return redirect('home')
    