from collections import defaultdict

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission, User
from django.shortcuts import render, redirect


def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('users')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, "login.html")
    else:
        # Render the login form
        return render(request, 'login.html')


def custom_logout(request):
    logout(request)
    return redirect('login')


@login_required
def users(request):
    all_users = User.objects.all()
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('user_email')
        password = request.POST.get('user_password')
        username = request.POST.get('user_email')
        is_superuser = False
        is_active = True
        is_staff = True
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_superuser = is_superuser
        user.is_active = is_active
        user.is_staff = is_staff
        user.save()
        messages.success(request, "User Added successfully")
    context = {

        'users': all_users
    }

    return render(request, template_name='users/users.html', context=context)


@login_required
def update_user(request):
    id = request.POST.get('user_id')
    user = User.objects.get(pk=id)

    # Get data from POST request
    email = request.POST.get('user_email')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    password = request.POST.get('user_password')

    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.password = make_password(password)
    user.username = email

    user.save()
    messages.success(request, "User updated successfully")
    return redirect('users')


@login_required
def delete_user(request, id):
    User.objects.get(id=id).delete()
    messages.error(request, "User deleted successfully")
    return redirect('users')


@login_required
def permissions(request):
    all_permissions = Permission.objects.filter(content_type_id__in=[2, 4]).select_related(
        'content_type')
    grouped_permissions = defaultdict(list)
    for perm in all_permissions:
        grouped_permissions[perm.content_type.name].append(perm)

    context = {
        'grouped_permissions': dict(grouped_permissions),
    }
    return render(request, template_name="users/permission.html", context=context)




@login_required
def assign_permission(request):
    all_permissions = Permission.objects.filter(content_type_id__in=[2, 4]).select_related(
        'content_type')
    permissions_grouped = defaultdict(list)

    for perm in all_permissions:
        permissions_grouped[perm.content_type].append(perm)

    all_users = User.objects.all()
    context = {
        'permissions_grouped': dict(permissions_grouped),
        'users': all_users
    }
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        permission_ids = request.POST.getlist('permissions_id')
        user = User.objects.get(pk=user_id)
        permissions = Permission.objects.filter(pk__in=permission_ids)
        for permission in permissions:
            user.user_permissions.add(permission)
    return render(request, template_name="users/assign_permission.html", context=context)


@login_required
def edit_user_permission(request, id):
    user = User.objects.get(id=id)
    all_permissions = Permission.objects.filter(content_type_id__in=[2, 4]).select_related(
        'content_type')
    user_permissions_set = set(user.user_permissions.all().values_list('id', flat=True))

    permissions_grouped = defaultdict(list)
    for perm in all_permissions:
        permissions_grouped[perm.content_type.name].append(perm)

    context = {
        'selected_user': user,
        'permissions_grouped': dict(permissions_grouped),
        'user_permissions': user_permissions_set,
    }
    return render(request, template_name="users/update_user_permission.html", context=context)


@login_required
def update_user_permissions(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        submitted_permissions_ids = set(map(int, request.POST.getlist('permissions_id')))

        # Current permissions assigned to the user
        current_permissions = set(user.user_permissions.all().values_list('id', flat=True))

        # Determine permissions to add (new ones that are in submitted but not in current)
        permissions_to_add = submitted_permissions_ids - current_permissions

        # Determine permissions to remove (those that are in current but not in submitted)
        permissions_to_remove = current_permissions - submitted_permissions_ids

        # Apply changes to the user's permissions
        if permissions_to_add:
            user.user_permissions.add(*permissions_to_add)
        if permissions_to_remove:
            user.user_permissions.remove(*permissions_to_remove)
        messages.success(request, "Permissions updated successfully")
        return redirect('users')
    else:
        return redirect('users')
