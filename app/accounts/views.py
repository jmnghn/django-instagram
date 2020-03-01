from django.contrib import messages
from django.contrib.auth import login as django_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    logout_then_login,
    LogoutView,
    PasswordChangeView as AuthPasswordChangeView
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .forms import SignupForm, ProfileForm, PasswordChangeForm
from .models import User

login = LoginView.as_view(template_name='accounts/login_form.html')


# logout = LogoutView.as_view(next_page='/accounts/')
@login_required
def user_follow(request, username):
    follow_user = get_object_or_404(User, username=username, is_active=True)

    request.user.following_set.add(follow_user)
    follow_user.follower_set.add(request.user)

    messages.success(request, f'{follow_user}을 follow 했습니다.')
    redirect_url = request.META.get('HTTP_REFERER', 'instagram:index')
    return redirect(redirect_url)


@login_required
def user_unfollow(request, username):
    unfollow_user = get_object_or_404(User, username=username, is_active=True)

    request.user.following_set.remove(unfollow_user)
    unfollow_user.follower_set.remove(request.user)

    messages.success(request, f'{unfollow_user}을 unfollow 했습니다.')
    redirect_url = request.META.get('HTTP_REFERER', 'instagram:index')
    return redirect(redirect_url)


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


class PasswordChangeView(LoginRequiredMixin, AuthPasswordChangeView):
    success_url = reverse_lazy('password_change')
    template_name = 'accounts/password_change_form.html'
    form_class = PasswordChangeForm

    def form_valid(self, form):
        messages.success(self.request, '암호 변경')
        return super().form_valid(form)


password_change = PasswordChangeView.as_view()
