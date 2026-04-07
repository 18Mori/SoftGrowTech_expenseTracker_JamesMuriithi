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
    
    yesterday = today - timezone.timedelta(days=1)
    
    total_yesterday = Expense.objects.filter(created_at__date=yesterday).aggregate(Sum('amount'))['amount__sum'] or 0
    
    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        transaction_type = request.POST.get('transaction_type')
        
        
        Expense.objects.create(
            amount=amount,
            category=category,
            title=title,
            transaction_type=transaction_type
        )
        return redirect('home')
    
    expenses = Expense.objects.all().order_by('-created_at')
    
    
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
        'total_yesterday': total_yesterday,
        'is_today': True,
    })

def history(request):
    sort_by = request.GET.get('sort', '-date')
    category_filter = request.GET.get('category')
    
    all_expenses = Expense.objects.all()
    
    if category_filter:
        all_expenses = all_expenses.filter(category=category_filter)
        
    all_expenses = all_expenses.order_by(sort_by, '-created_at')
    
    context = {
        'expenses': all_expenses,
        'is_history': True,
        'categories': Expense.objects.values_list('category', flat=True).distinct()
    }
    return render(request, 'history.html', context)
    
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, id=pk)
    if request.method == 'POST':
        expense.delete()
        messages.warning(request, "Deleted.")
    return redirect('home')
    