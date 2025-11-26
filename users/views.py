# ...existing code...
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def logout_view(request):
    """Log the user out."""
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))

def login_view(request):
    """Handle login form (POST) and show login page (GET)."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next')
            if user.is_staff or user.is_superuser:
                return redirect('admin:index')
            return redirect(next_url or 'learning_logs:index')
        messages.error(request, 'Tên đăng nhập hoặc mật khẩu sai.')
    else:
        form = AuthenticationForm(request)
    return render(request, 'users/login.html', {'form': form})

def register(request):
    """Register a new user."""
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            user = authenticate(request, username=form.cleaned_data['username'],
                                         password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
            messages.success(request, 'Tạo tài khoản thành công.')
            return redirect('learning_logs:index')
    context = {'form': form}
    return render(request, 'users/register.html', context)
# ...existing code...