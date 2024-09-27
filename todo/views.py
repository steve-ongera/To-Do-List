from django.shortcuts import render, redirect , get_object_or_404
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm


@login_required
def index(request):
    tasks = Task.objects.filter(user=request.user)  # Only tasks for the current user
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Associate the task with the current user
            task.save()
            messages.success(request, 'Task added successfully!')
            return redirect('index')

    context = {'tasks': tasks, 'form': form}
    return render(request, 'index.html', context)


@login_required
def update_task(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('index')

    context = {'form': form}
    return render(request, 'update_task.html', context)

@login_required
def task_detail(request, task_id):
    # Fetch the specific task or return a 404 if not found
    task = get_object_or_404(Task, id=task_id, user=request.user)  # Ensure the task belongs to the user
    return render(request, 'task_detail.html', {'task': task})


@login_required
def delete_task(request, pk):
    task = Task.objects.get(id=pk, user=request.user)

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('index')

    context = {'task': task}
    return render(request, 'delete_task.html', context)


@login_required
def add_task(request):
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Associate the task with the current user
            task.save()
            messages.success(request, 'Task added successfully!')
            return redirect('index')  # Redirect to the task list page after adding

    context = {'form': form}
    return render(request, 'add_task.html', context)


# User Registration View
# User Registration View
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Create the user
            user = User.objects.create_user(username=username, password=password)
            login(request, user)  # Automatically log in the user
            messages.success(request, 'Registration successful! You are now logged in.')
            return redirect('index')  # Redirect to the index page after registration
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

# User Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('index')  # Redirect to the index page after login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')

# User Logout View
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('user_login')  # Redirect to the login page after logout



@login_required
def profile_update(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile_update')  # Redirect to the same page after updating
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'profile_update.html', context)
