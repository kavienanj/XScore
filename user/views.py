from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from .forms import SignUpForm

# Create your views here.


def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:  # return redirect('login') 'status': 'Signing Up Successful Login to Continue'
                return redirect('login')
            else:
                form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})
