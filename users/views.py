from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
#from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import Group
from .models import CustomUser

def logout_view(request):
    """Log the user out."""
    logout(request)
    return HttpResponseRedirect(reverse('eLearn:index'))

def register(request):
    """Register a new user."""
    if request.method != 'POST':
        # Display blank registration form.
        form = CustomUserCreationForm()
    else:
        # Process completed form.
        form = CustomUserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Log the user in and then redirect to home page.
            authenticated_user = authenticate(username=new_user.username,
                password=request.POST['password1'])
            
            if authenticated_user.userType == 2:
                el_professors_group = Group.objects.get(name='Professors')
                el_professors_group.user_set.add(authenticated_user)
                # if authenticated_user.PIN != '201901':
                #     print('PIN wrong! Please recheck it.')
                #     context = {'form': form}
                #     return render(request, 'users/register.html', context)
                #     return HttpResponseRedirect(reverse('eLearn:main'))
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('eLearn:main'))

    context = {'form': form}
    return render(request, 'users/register.html', context)

