from datetime import datetime

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import *
from .utils import *


class PostListView(LoginRequiredMixin, ListView):
    paginate_by = 3
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    ordering = ['-modified_date']
    raise_exception = True

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_by = self.request.GET.get('filter_by')
        if filter_by == 'delayed':
            queryset = queryset.filter(publication_date__isnull=False, is_published=False)
        elif filter_by == 'published':
            queryset = queryset.filter(publication_date__isnull=False, is_published=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = datetime.now()
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')
    template_name = 'posts/post_confirm_delete.html'
    raise_exception = True

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_update.html'

    success_url = reverse_lazy('post_list')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

    context_object_name = 'post'


class PostPublishView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostPublishForm
    template_name = 'posts/post_publish.html'
    context_object_name = 'post'
    raise_exception = True

    success_url = reverse_lazy('post_list')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def form_valid(self, form):
        post = form.save(commit=False)
        # post.is_published = True
        if not post.publication_date:
            post.publication_date = timezone.now()
        post.modified_date = timezone.now()
        post.save()
        return super().form_valid(form)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def post_un_publish_view(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Изменяем значения is_published и publication_date
    post.is_published = False
    post.publication_date = None
    post.save()

    return redirect('post_list')


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = PostForm
    template_name = 'posts/post_create.html'

    success_url = reverse_lazy('post_list')
    raise_exception = True

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_cover(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.cover:
        post.cover.delete()
        post.cover = None
        post.save()

    return redirect(reverse('post_update', args=[pk]))


class RegisterUserView(CreateView):
    form_class = RegisterUserForm
    template_name = 'posts/auth/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('post_list')


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'posts/auth/login.html'

    def get_success_url(self):
        return reverse_lazy('post_list')


def logout_user(request):
    logout(request)
    return redirect('login')


def tr_handler404(request, exception):
    """
    Обработка ошибки 404
    """
    return render(request=request, template_name='posts/exceptions/error_page.html', status=404, context={
        'title': 'Страница не найдена: 404',
        'error_message': 'К сожалению такая страница была не найдена, или перемещена',
    })


def tr_handler500(request):
    """
    Обработка ошибки 500
    """
    return render(request=request, template_name='posts/exceptions/error_page.html', status=500, context={
        'title': 'Ошибка сервера: 500',
        'error_message':
            'Внутренняя ошибка сайта, вернитесь на главную страницу, отчет об ошибке мы направим администрации сайта',
    })


def tr_handler403(request, exception):
    """
    Обработка ошибки 403
    """
    if request.user.is_authenticated:
        return redirect('post_list')
    else:
        return redirect('login')
    # return render(request=request, template_name='posts/exceptions/error_page.html', status=403, context={
    #     'title': 'Ошибка доступа: 403',
    #     'error_message': 'Доступ к этой странице ограничен',
    # })
