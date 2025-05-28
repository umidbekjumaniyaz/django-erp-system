from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import Employee, Project, Task, Expense, Order
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from django import forms
from django.db import models

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'team_members', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.manager = kwargs.pop('manager', None)
        super().__init__(*args, **kwargs)
        if self.manager:
            self.fields['team_members'].queryset = Employee.objects.exclude(id=self.manager.id)
            self.fields['team_members'].required = False  # Team members is now optional

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'due_date', 'status', 'priority']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        assigned_to = kwargs.pop('assigned_to', None)
        super().__init__(*args, **kwargs)
        if assigned_to:
            # Show projects where the user is either a team member or the manager
            self.fields['project'].queryset = Project.objects.filter(
                models.Q(team_members=assigned_to) | models.Q(manager=assigned_to)
            ).distinct()

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['project', 'description', 'amount', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        submitted_by = kwargs.pop('submitted_by', None)
        super().__init__(*args, **kwargs)
        if submitted_by:
            # Show projects where the user is either a team member or the manager
            self.fields['project'].queryset = Project.objects.filter(
                models.Q(team_members=submitted_by) | models.Q(manager=submitted_by)
            ).distinct()
            # Add Select2 classes and attributes
            self.fields['project'].widget.attrs.update({
                'class': 'select2',
                'data-placeholder': 'Select a project',
            })

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'customer_phone', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['customer_email'].widget.attrs.update({'class': 'form-control'})
        self.fields['customer_phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['notes'].widget.attrs.update({'class': 'form-control'})

@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            # Generate order number (using timestamp to ensure uniqueness)
            order.order_number = f'ORD-{timezone.now().strftime("%Y%m%d-%H%M%S")}'
            order.created_by = request.user.employee
            order.save()
            messages.success(request, 'Order created successfully!')
            return redirect('erp_core:dashboard')
    else:
        form = OrderForm()
    
    return render(request, 'erp_core/order_form.html', {'form': form})

@login_required
def order_list(request):
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'erp_core/order_list.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'erp_core/order_detail.html', {'order': order})

def create_employee(request):
    if request.user.is_authenticated and not hasattr(request.user, 'employee'):
        Employee.objects.create(
            user=request.user,
            department='Administration',
            position='Admin',
            phone='N/A',
            hire_date=timezone.now().date()
        )
    return redirect('erp_core:dashboard')

@login_required
def dashboard(request):
    if not hasattr(request.user, 'employee'):
        return redirect('erp_core:create_employee')
    
    try:
        employee = request.user.employee
        context = {
            'projects': Project.objects.filter(team_members=employee)[:5],
            'tasks': Task.objects.filter(assigned_to=employee, status__in=['todo', 'in_progress'])[:5],
            'expenses': Expense.objects.filter(submitted_by=employee)[:5]
        }
    except Employee.DoesNotExist:
        context = {}
    return render(request, 'erp_core/dashboard.html', context)

@login_required
def project_list(request):
    projects = Project.objects.all()  # Show all projects instead of filtering
    return render(request, 'erp_core/project_list.html', {'projects': projects})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    completed_tasks = project.tasks.filter(status='done').count()
    in_progress_tasks = project.tasks.filter(status='in_progress').count()
    total_expenses = sum(expense.amount for expense in project.expenses.all())
    
    context = {
        'project': project,
        'completed_tasks': completed_tasks,
        'in_progress_tasks': in_progress_tasks,
        'total_expenses': total_expenses
    }
    return render(request, 'erp_core/project_detail.html', context)

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, manager=request.user.employee)
        if form.is_valid():
            project = form.save(commit=False)
            project.manager = request.user.employee
            project.save()
            # Add the manager to team_members automatically
            project.team_members.add(request.user.employee)
            form.save_m2m()  # Save other team members
            messages.success(request, 'Project created successfully!')
            return redirect('erp_core:project_detail', pk=project.pk)
    else:
        form = ProjectForm(manager=request.user.employee)
    return render(request, 'erp_core/project_form.html', {'form': form})

@login_required
def task_list(request):
    employee = request.user.employee
    tasks = Task.objects.filter(assigned_to=employee)
    return render(request, 'erp_core/task_list.html', {'tasks': tasks})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'erp_core/task_detail.html', {'task': task})

@login_required
def task_create(request):
    project_id = request.GET.get('project')
    initial_data = {}
    
    if project_id:
        try:
            project = Project.objects.get(id=project_id)
            initial_data['project'] = project
        except Project.DoesNotExist:
            pass
    
    if request.method == 'POST':
        form = TaskForm(request.POST, assigned_to=request.user.employee)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_to = request.user.employee
            task.save()
            messages.success(request, 'Task created successfully!')
            
            # Redirect back to project detail if project_id was provided
            if project_id:
                return redirect('erp_core:project_detail', pk=project_id)
            return redirect('erp_core:task_detail', pk=task.pk)
    else:
        form = TaskForm(assigned_to=request.user.employee, initial=initial_data)
    return render(request, 'erp_core/task_form.html', {'form': form})

@login_required
def expense_list(request):
    employee = request.user.employee
    expenses = Expense.objects.filter(submitted_by=employee).order_by('-date')  # Yangi xarajatlar yuqorida
    return render(request, 'erp_core/expense_list.html', {'expenses': expenses})


@login_required
def expense_detail(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    return render(request, 'erp_core/expense_detail.html', {'expense': expense})

@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, submitted_by=request.user.employee)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.submitted_by = request.user.employee
            expense.status = 'pending'
            expense.save()
            messages.success(request, 'Expense submitted successfully!')
            return redirect('erp_core:expense_list')
    else:
        form = ExpenseForm(submitted_by=request.user.employee)
    return render(request, 'erp_core/expense_form.html', {'form': form})

@login_required
def profile(request):
    employee = request.user.employee
    return render(request, 'erp_core/profile.html', {'employee': employee})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if not hasattr(user, 'employee'):
                return redirect('erp_core:create_employee')
            return redirect('erp_core:dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'erp_core/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('erp_core:login')

@login_required
def retail_dashboard(request):
    # Sample data for retail dashboard
    context = {
        'daily_sales': 24750,
        'weekly_sales': 168400,
        'monthly_sales': 720500,
        'inventory_count': 5842,
        'new_customers': 1284,
        'orders_today': 847,
        'low_stock_items': [
            {'name': 'Premium Denim Jeans', 'stock': 8, 'sizes': 'M, L'},
            {'name': 'Summer Collection T-Shirts', 'stock': 5, 'sizes': 'S'},
            {'name': 'Designer Leather Jackets', 'stock': 0, 'sizes': 'All'}
        ],
        'best_sellers': [
            {'name': 'Premium Jeans', 'units': 452},
            {'name': 'Designer Shirts', 'units': 378},
            {'name': 'Summer Dresses', 'units': 325},
            {'name': 'Leather Jackets', 'units': 290},
            {'name': 'Casual T-Shirts', 'units': 262}
        ],
        'categories': [
            {'name': "Men's Wear", 'items': 420},
            {'name': "Women's Wear", 'items': 380},
            {'name': "Kids' Wear", 'items': 220},
            {'name': 'Accessories', 'items': 160}
        ],
        'monthly_sales_data': [65000, 59000, 80000, 81000, 86000, 95000, 89000, 96000, 98000, 92000, 95000, 98000]
    }
    return render(request, 'erp_core/retail_dashboard.html', context)
