from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("my-posts/", views.MyPostsView.as_view(), name="my_posts"),

    path("register/", views.RegisterView.as_view(), name="register"),

    path("posts/new/", views.PostCreateView.as_view(), name="post_create"),

    path(
        "posts/<slug:slug>/edit/",
        views.PostUpdateView.as_view(),
        name="post_edit",
    ),

    path(
        "posts/<slug:slug>/delete/",
        views.PostDeleteView.as_view(),
        name="post_delete",
    ),

    path(
        "posts/<slug:slug>/",
        views.PostDetailView.as_view(),
        name="post_detail",
    ),

    path("about/", views.about, name="about"),

    path("contact/", views.contact, name="contact"),

    # Password Reset
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="blog/password_reset_form.html",
            email_template_name="registration/password_reset_email.html",
            success_url="/password-reset/done/",
        ),
        name="password_reset",
    ),

    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url="/reset/done/",
        ),
        name="password_reset_confirm",
    ),

    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]