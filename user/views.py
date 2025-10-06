from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages as message
from django.contrib.auth.decorators import login_required
from reports.models import Found_reports, Lost_reports, Claimed_items
# Create your views here.


def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        user_name = request.POST.get('username')
        student_id = request.POST.get('student_id')
        phone = request.POST.get('phone')
        dept = request.POST.get('dept')
        profile_pic = request.FILES.get('profile_pic')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=user_name).exists():
            message.error(request, 'Username already exists.')
            return redirect('user:register')
        
        elif User.objects.filter(email=email).exists():
            message.error(request, 'Email already exists.')
            return redirect('user:register')

        elif Profile.objects.filter(student_id=student_id).exists():
            message.error(request, 'Student ID already exists.')
            return redirect('user:register')

        elif password1 != password2:
            message.error(request, 'Passwords do not match.')
            return redirect('user:register')
        else:
            user = User.objects.create_user(
                username=user_name,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )

            Profile.objects.create(
                user=user,
                student_id=student_id,
                phone=phone,
                dept=dept,
                profile_picture=profile_pic
            )

            message.success(request, 'Registration successful.')
            return redirect('user:login')
    else:
       return render(request, 'users/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                message.success(request, 'Login successful')
                return redirect('user:profile')

            else:
                message.error(request, 'Invalid username or password')
                return redirect('user:login')

        except User.DoesNotExist:
            message.error(request, 'Invalid username or password')
            return redirect('user:login')
    else:
        return render(request, 'users/login.html')





@login_required(login_url='user:login')
def profile_view(request):
    user = request.user

    # If user is superuser → redirect to admin dashboard
    if user.is_superuser:
        return redirect('user:admin_dashboard')

    # Otherwise → show normal profile
    return render(request, 'users/profile.html', {'user': user})


@login_required(login_url='user:login')
def admin_dashboard(request):
    # Only allow superusers to access this page
    if not request.user.is_superuser:
        return redirect('user:profile_view')

    # Fetch all users
    users = User.objects.all()
    found_reports = Found_reports.objects.all()
    lost_reports = Lost_reports.objects.all()
    claimed_items = Claimed_items.objects.all()


    return render(request, 'users/admin_dashboard.html', {'users': users, 'found_reports': found_reports, 'lost_reports': lost_reports, 'claimed_items': claimed_items})


def logout_view(request):
    logout(request)
    message.success(request, 'Logout successful')
    return redirect('user:login')

def user_list(request):
    if not request.user.is_superuser:
        return redirect('user:profile_view')

    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})


@login_required(login_url='user:login')
def profile_edit_view(request):
    user = request.user
    Profile = user.profile  
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dept = request.POST.get('dept')
        profile_pic = request.FILES.get('profile_pic')
        if email:
            user.email = email
            user.save()

        # Update Profile model
        if phone:
            Profile.phone = phone
        if dept:
            Profile.dept = dept
        if profile_pic:
            Profile.profile_picture = profile_pic
        Profile.save()

        message.success(request, 'Profile updated successfully.')
        return redirect('user:profile')

    return render(request, 'users/edit_profile.html', {'user': user, 'profile': user.profile})