from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Task
from .forms import TaskForm

# view for custom login
def custom_login(request):
    if request.user.is_authenticated:
        return redirect('tasks')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('tasks')
    else:
        form = AuthenticationForm()

    return render(request, 'base/login.html', {'form': form})

# view for user registration
def register_page(request):
    if request.user.is_authenticated:
        return redirect('tasks')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return redirect('tasks')
    else:
        form = UserCreationForm()

    return render(request, 'base/register.html', {'form': form})

# view for task list
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    count = tasks.filter(complete=False).count()

    search_input = request.GET.get('search-area', '')
    if search_input:
        tasks = tasks.filter(title__startswith=search_input)

    return render(request, 'base/task_list.html', {
        'tasks': tasks,
        'count': count,
        'search_input': search_input,
    })

# view for task detail
@login_required
def task_detail(request, pk):
    task = Task.objects.get(pk=pk)
    return render(request, 'base/task.html', {'task': task})

# view for creating a task
@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('tasks')
    else:
        form = TaskForm()

    return render(request, 'base/task_form.html', {'form': form})

# view for updating a task
@login_required
def task_update(request, pk):
    task = Task.objects.get(pk=pk)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks')
    else:
        form = TaskForm(instance=task)

    return render(request, 'base/task_form.html', {'form': form})

# view for deleting a task
@login_required
def task_delete(request, pk):
    task = Task.objects.get(pk=pk)
    
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

    return render(request, 'base/task_confirm_delete.html', {'task': task})
