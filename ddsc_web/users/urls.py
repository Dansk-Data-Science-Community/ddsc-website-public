from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .forms import PasswordResetForm, SetPasswordForm, ChangePasswordForm

app_name = "users"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("edit/", views.edit, name="edit"),
    path("edit_image", views.edit_image, name="edit_image"),
    path("delete_image", views.delete_image, name="delete_image"),
    path(
        "password_change_done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="auth/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path("login/", views.UserLogin.as_view(), name="login"),
    path("logout/", views.user_logout, name="logout"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="auth/password_reset_form.html",
            email_template_name="auth/password_reset_email.html",
            form_class=PasswordResetForm,
            success_url="/users/password_reset_done",
        ),
        name="password_reset",
    ),
    path(
        "password_reset_done",
        auth_views.PasswordResetDoneView.as_view(
            template_name="auth/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "password_reset_confirm/<str:uidb64>/<str:token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="auth/password_reset_confirm.html",
            form_class=SetPasswordForm,
            success_url="/users/password_reset_complete",
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="auth/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="auth/password_change_form.html",
            form_class=ChangePasswordForm,
            success_url="/users/password_change_done",
        ),
        name="password_change",
    ),
    path("activate/<str:uidb64>/<str:token>", views.activate, name="activate"),
]
