from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from core.services.auth_service import AuthService


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect("project_list")

    if request.method == "GET":
        return render(
            request,
            "auth/login.html",
            {
                "form_data": {"username": ""},
                "errors": {},
                "next_url": request.GET.get("next", ""),
            },
        )

    form_data = {
        "username": request.POST.get("username", ""),
    }
    next_url = request.POST.get("next", "")
    user, errors = AuthService().login(
        form_data["username"],
        request.POST.get("password", ""),
    )
    if errors:
        return render(
            request,
            "auth/login.html",
            {
                "form_data": form_data,
                "errors": errors,
                "next_url": next_url,
            },
        )

    auth_login(request, user)
    messages.success(request, "Welcome back.")
    if next_url:
        return redirect(next_url)
    return redirect("project_list")


@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.user.is_authenticated:
        return redirect("project_list")

    if request.method == "GET":
        return render(
            request,
            "auth/register.html",
            {
                "form_data": {"username": ""},
                "errors": {},
            },
        )

    form_data = {
        "username": request.POST.get("username", ""),
    }
    user, errors = AuthService().register(
        form_data["username"],
        request.POST.get("password", ""),
        request.POST.get("password_confirm", ""),
    )
    if errors:
        return render(
            request,
            "auth/register.html",
            {
                "form_data": form_data,
                "errors": errors,
            },
        )

    auth_login(request, user)
    messages.success(request, "Account created. You are now signed in.")
    return redirect("project_list")


@require_http_methods(["POST"])
def logout_view(request):
    auth_logout(request)
    messages.success(request, "You have been signed out.")
    return redirect("login")
