from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PostForm
from .models import Tag, Post


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post.tag_set.add(*post.extract_tag_list()) # list 로 add 하니까 개별로 들어가내...
            messages.success(request, '포스팅 저장')
            return redirect(post) # get_absolute_url
    else:
        form = PostForm()
    return render(request, 'instagram/post_new_form.html', {
        'form': form,
    })


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'instagram/post_detail.html', {
        'post': post,
    })