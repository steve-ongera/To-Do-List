# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import Profile, Task, TaskCategory
from .forms import (
    CustomUserCreationForm, ProfileForm, TaskForm, 
    PasswordChangeForm, TaskFilterForm
)


def home_view(request):
    """Home page - redirects to login if not authenticated"""
    if request.user.is_authenticated:
        return redirect('task_list')
    return redirect('login')


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('task_list')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create profile for new user
            Profile.objects.create(user=user)
            messages.success(request, 'Registration successful! Please set up your profile.')
            return redirect('setup_profile', user_id=user.id)
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


def setup_profile_view(request, user_id):
    """Initial profile setup after registration"""
    user = get_object_or_404(User, id=user_id)
    profile, created = Profile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile setup complete! You can now login.')
            return redirect('login')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'registration/setup_profile.html', {
        'form': form,
        'user': user
    })


def login_view(request):
    """Custom login view"""
    if request.user.is_authenticated:
        return redirect('task_list')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'task_list')
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'registration/login.html')


@login_required
def logout_view(request):
    """Logout view"""
    username = request.user.username
    logout(request)
    messages.info(request, f'Goodbye, {username}!')
    return redirect('login')


@login_required
def task_list_view(request):
    """Main task list view with filtering and search"""
    tasks = Task.objects.filter(user=request.user)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        if status_filter == 'completed':
            tasks = tasks.filter(completed=True)
        elif status_filter == 'pending':
            tasks = tasks.filter(completed=False)
        elif status_filter in [choice[0] for choice in Task.STATUS_CHOICES]:
            tasks = tasks.filter(status=status_filter)
    
    # Filter by category
    category_filter = request.GET.get('category', '')
    if category_filter:
        tasks = tasks.filter(category_id=category_filter)
    
    # Filter by priority
    priority_filter = request.GET.get('priority', '')
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    
    # Ordering
    order_by = request.GET.get('order_by', '-created_at')
    if order_by in ['created_at', '-created_at', 'due_date', '-due_date', 'priority', 'title']:
        tasks = tasks.order_by(order_by)
    
    # Pagination
    paginator = Paginator(tasks, 10)
    page_number = request.GET.get('page')
    tasks_page = paginator.get_page(page_number)
    
    # Get categories for filter dropdown
    categories = TaskCategory.objects.all()
    
    # Statistics
    total_tasks = Task.objects.filter(user=request.user).count()
    completed_tasks = Task.objects.filter(user=request.user, completed=True).count()
    pending_tasks = total_tasks - completed_tasks
    overdue_tasks = Task.objects.filter(
        user=request.user, 
        completed=False, 
        due_date__lt=timezone.now()
    ).count()
    
    context = {
        'tasks': tasks_page,
        'categories': categories,
        'search_query': search_query,
        'status_filter': status_filter,
        'category_filter': category_filter,
        'priority_filter': priority_filter,
        'order_by': order_by,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,
        'priority_choices': Task.PRIORITY_CHOICES,
        'status_choices': Task.STATUS_CHOICES,
    }
    
    return render(request, 'tasks/task_list.html', context)


@login_required
def task_create_view(request):
    """Create new task view"""
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, f'Task "{task.title}" created successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()
    
    return render(request, 'tasks/task_form.html', {
        'form': form,
        'title': 'Create New Task',
        'button_text': 'Create Task'
    })


@login_required
def task_update_view(request, task_id):
    """Update existing task view"""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Task "{task.title}" updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'tasks/task_form.html', {
        'form': form,
        'task': task,
        'title': f'Update Task: {task.title}',
        'button_text': 'Update Task'
    })


@login_required
def task_delete_view(request, task_id):
    """Delete task view"""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    if request.method == 'POST':
        task_title = task.title
        task.delete()
        messages.success(request, f'Task "{task_title}" deleted successfully!')
        return redirect('task_list')
    
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


@login_required
def task_detail_view(request, task_id):
    """Task detail view"""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})


@login_required
def toggle_task_status(request, task_id):
    """AJAX view to toggle task completion status"""
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.completed = not task.completed
        task.save()
        
        return JsonResponse({
            'success': True,
            'completed': task.completed,
            'completed_at': task.completed_at.isoformat() if task.completed_at else None
        })
    
    return JsonResponse({'success': False})


@login_required
def profile_view(request):
    """View user profile"""
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'users/profile.html', {'profile': profile})


@login_required
def profile_update_view(request):
    """Update user profile"""
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'users/profile_form.html', {
        'form': form,
        'profile': profile
    })


@login_required
def change_password_view(request):
    """Change user password"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Password changed successfully!')
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'users/change_password.html', {'form': form})


@login_required
def dashboard_view(request):
    """Dashboard with task statistics"""
    user_tasks = Task.objects.filter(user=request.user)
    
    # Recent tasks
    recent_tasks = user_tasks.order_by('-created_at')[:5]
    
    # Upcoming tasks
    upcoming_tasks = user_tasks.filter(
        completed=False, 
        due_date__isnull=False
    ).order_by('due_date')[:5]
    
    # Statistics
    stats = {
        'total_tasks': user_tasks.count(),
        'completed_tasks': user_tasks.filter(completed=True).count(),
        'pending_tasks': user_tasks.filter(completed=False).count(),
        'overdue_tasks': user_tasks.filter(
            completed=False, 
            due_date__lt=timezone.now()
        ).count(),
        'high_priority_tasks': user_tasks.filter(
            completed=False, 
            priority='high'
        ).count(),
    }
    
    # Tasks by category
    categories_stats = []
    for category in TaskCategory.objects.all():
        category_tasks = user_tasks.filter(category=category)
        if category_tasks.exists():
            categories_stats.append({
                'category': category,
                'total': category_tasks.count(),
                'completed': category_tasks.filter(completed=True).count(),
                'pending': category_tasks.filter(completed=False).count(),
            })
    
    context = {
        'recent_tasks': recent_tasks,
        'upcoming_tasks': upcoming_tasks,
        'stats': stats,
        'categories_stats': categories_stats,
    }
    
    return render(request, 'dashboard/dashboard.html', context)