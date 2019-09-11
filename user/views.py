from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def logout(request, *args, **kwargs):
    return auth_views.LogoutView.as_view(template_name='users/logged_out.html')(request, *args, **kwargs)


def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})
