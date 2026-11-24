from django.conf import settings
from django.shortcuts import redirect


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if request.user.is_authenticated:
            return self.get_response(request)

        if path.startswith("/static/"):
            return self.get_response(request)
        if path.startswith("/admin/"):
            return self.get_response(request)

        open_paths = [
            "/accounts/login/",
            "/accounts/register/",
        ]
        for open_path in open_paths:
            if path == open_path:
                return self.get_response(request)

        login_url = settings.LOGIN_URL
        return redirect(login_url + "?next=" + path)
