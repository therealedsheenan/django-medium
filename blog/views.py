from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm, UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView
)


class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    template_name = 'blog/post/list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    template_name = 'blog/post/detail.html'
    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):
    template_name = 'blog/post/form.html'
    login_url = '/login/'
    redirect_field_name = 'blog/post/detail.html'

    form_class = PostForm
    model = Post


class UpdatePostView(LoginRequiredMixin, UpdateView):
    template_name = 'blog/post/form.html'
    login_url = '/login/'
    redirect_field_name = 'blog/post/detail.html'

    form_class = PostForm
    model = Post


class DraftListView(LoginRequiredMixin, ListView):
    template_name = 'blog/post/list.html'
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True)


# Remove post
@login_required()
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog:post_list')


# Comments
@login_required()
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish_update()
    return redirect('blog:post_detail', pk=pk)


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment/form.html', {'form': form})


@login_required()
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve_comment()
    return redirect('blog:post_detail', pk=comment.post.pk)


@login_required()
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog:post_detail', pk=post_pk)


# Login and Registration
@login_required
def user_logout(request):
    logout(request)
    return redirect('/')


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)

        if form.is_valid():
            user = form.save(commit=True)
            user.set_password(user.password)
            user.save()
            return redirect('blog:post_list')
    else:
        form = UserRegistrationForm

    return render(request, "registration/register.html", {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('blog:post_list')
    else:
        return render(request, "registration/login.html", {})
