from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.urls import reverse
from .models import Account

# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    next_url = request.GET.get('next', '')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        next_url = request.POST.get('next', '') or request.GET.get('next', '')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect(next_url if next_url else 'home')
        else:
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'accounts/login.html', {'next': next_url})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    next_url = request.GET.get('next', '')
    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        next_url = request.POST.get('next', '') or request.GET.get('next', '')
        
        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/register.html', {'next': next_url})
        
        if Account.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'accounts/register.html', {'next': next_url})
        
        if Account.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'accounts/register.html', {'next': next_url})
        
        # Create user
        user = Account.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password
        )
        
        messages.success(request, 'Account created successfully! Please login.')
        login_url = reverse('login')
        if next_url:
            login_url = f"{login_url}?next={next_url}"
        return redirect(login_url)
    
    return render(request, 'accounts/register.html', {'next': next_url})


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')


from django.contrib.auth.decorators import login_required
from workspaces.models import Workspace

@login_required
def profile_view(request):
    user = request.user
    
    # Count total workspaces created by user
    total_workspaces = Workspace.objects.filter(creator=user).count()
    
    # Count workspaces where user is a member
    member_workspaces = user.workspace_memberships.count()
    
    context = {
        'user': user,
        'total_workspaces': total_workspaces,
        'member_workspaces': member_workspaces,
    }
    
    return render(request, 'accounts/profile.html', context)