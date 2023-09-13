from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreationUserForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def start_app(request):
    return redirect('login')


def register(request,pk):
    if request.method == 'POST':
        form = CreationUserForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(
                request, f'{username} Registered successfully!', extra_tags='success')
            return redirect('login')
        else:
            form = CreationUserForm(request=request)
            # Concatenate form errors into a single string
            form_errors = ', '.join(
                str(error) for field_errors in form.errors.values() for error in field_errors)
            messages.error(request, form_errors)
            messages.warning(request, 'Please correct the errors below.')
    else:
        form = CreationUserForm(request=request)
        context = {
            'form': form,
            'messages': messages.get_messages(request)
        }
        return render(request, 'accounts/register.html', context)

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            username = user.username
            request.session['username'] = username
            if user.is_superuser:
                request.session['username'] = username
                messages.success(request, 'Welcome ' +
                                 username, extra_tags='success')
                return redirect('/Admin/')
            else:
                messages.success(request, 'Welcome ' +
                                 username, extra_tags='success')
                request.session['username'] = username
                return redirect('/Employee/')
        else:
            messages.warning(request, 'Wrong login credentials',
                             extra_tags='warning')
            return redirect('login')

    return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('login')
