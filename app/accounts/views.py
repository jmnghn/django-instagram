from django.contrib import messages
from django.contrib.auth import login as django_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, logout_then_login, LogoutView
from django.shortcuts import render, redirect

from .forms import SignupForm, ProfileForm

login = LoginView.as_view(template_name='accounts/login_form.html')


# logout = LogoutView.as_view(next_page='/accounts/')


def logout(request):
    messages.success(request, '로그아웃')
    return logout_then_login(request)


def temp(request):
    return render(request, 'accounts/temp.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            signuped_user = form.save()
            messages.success(request, '가입')
            django_login(request, signuped_user)
            # signed_user.send_welcome_email()  # Celery
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = SignupForm()
    return render(request, 'accounts/signup_form.html', {
        'form': form,
    })


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '프로필을 수정/저장했습니다.')
            return redirect('profile_edit')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile_edit_form.html', {
        'form': form,
    })
