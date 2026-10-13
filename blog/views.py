
from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)

from .models import Post, Category
from .forms import PostForm, RegisterForm


def home(request):
    query = request.GET.get("q", "")
    category_id = request.GET.get("category", "")

    # Show published posts only
    posts_list = Post.objects.filter(status="published")

    if query:
        posts_list = posts_list.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
        )

    if category_id.isdigit():
        posts_list = posts_list.filter(
            category__id=category_id
        )

    posts_list = posts_list.order_by("-created_at")

    categories = Category.objects.annotate(
        post_count=Count("posts")
    )

    paginator = Paginator(posts_list, 6)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "categories": categories,
        "query": query,
        "category_id": category_id,
    }

    return render(request, "blog/home.html", context)


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(
            status="published"
        ).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.annotate(
            post_count=Count("posts")
        )
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        queryset = Post.objects.all()

        if self.request.user.is_authenticated:
            return queryset.filter(
                Q(status="published")
                | Q(author=self.request.user)
            )

        return queryset.filter(status="published")


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = "login"

    def form_valid(self, form):
        form.instance.author = self.request.user

        response = super().form_valid(form)

        messages.success(
            self.request,
            "Post created successfully!"
        )

        return response

    def get_success_url(self):
        return reverse_lazy(
            "post_detail",
            kwargs={"slug": self.object.slug},
        )


class PostUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView,
):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = "login"

    def test_func(self):
        return (
            self.get_object().author_id
            == self.request.user.pk
        )

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "post_detail",
            kwargs={"slug": self.object.slug},
        )


class PostDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView,
):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    login_url = "login"
    success_url = reverse_lazy("home")

    def test_func(self):
        return (
            self.get_object().author_id
            == self.request.user.pk
        )

    def form_valid(self, form):
        messages.success(self.request, "Post deleted.")
        return super().form_valid(form)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "blog/register.html"
    success_url = "/"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)

        messages.success(
            self.request,
            "Registration successful!"
        )

        return response


class MyPostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog/my_posts.html"
    paginate_by = 6
    login_url = "login"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(
            author=self.request.user
        ).order_by("-created_at")


@login_required(login_url="login")
def my_posts(request):
    posts = Post.objects.filter(
        author=request.user
    ).order_by("-created_at")

    return render(
        request,
        "blog/post_list.html",
        {"posts": posts},
    )


def about(request):
    return render(
        request,
        "blog/about.html",
        {"team": "DjangoBlog Team"},
    )


def contact(request):
    return render(request, "blog/contact.html")


def custom_403(request, exception=None):
    return render(request, "blog/403.html", status=403)

def form_valid(self, form):
    form.instance.author = self.request.user
    messages.success(self.request, "Post published successfully!")
    return super().form_valid(form)
