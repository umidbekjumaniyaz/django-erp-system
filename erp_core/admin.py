from django.contrib import admin
from .models import Employee, Project, Task, Expense

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'position', 'phone', 'hire_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'department', 'position')
    list_filter = ('department', 'position')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'manager', 'status')
    search_fields = ('name', 'description', 'manager__user__username')
    list_filter = ('status', 'start_date', 'end_date')
    filter_horizontal = ('team_members',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assigned_to', 'due_date', 'status')
    search_fields = ('title', 'description', 'project__name', 'assigned_to__user__username')
    list_filter = ('status', 'due_date', 'project')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'project', 'amount', 'date', 'submitted_by', 'status')
    search_fields = ('description', 'project__name', 'submitted_by__user__username')
    list_filter = ('status', 'date', 'project')
