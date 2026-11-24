from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class AuthService:
    def register(self, username, password, password_confirm):
        clean_username = (username or "").strip()
        clean_password = password or ""
        clean_confirm = password_confirm or ""
        errors = {}

        if clean_username == "":
            errors["username"] = "Username is required."
        elif len(clean_username) < 3:
            errors["username"] = "Username must be at least 3 characters."
        elif User.objects.filter(username=clean_username).exists():
            errors["username"] = "This username is already taken."

        if clean_password == "":
            errors["password"] = "Password is required."
        elif len(clean_password) < 6:
            errors["password"] = "Password must be at least 6 characters."

        if clean_confirm == "":
            errors["password_confirm"] = "Please confirm the password."
        elif clean_password != clean_confirm:
            errors["password_confirm"] = "Passwords do not match."

        if errors:
            return None, errors

        user = User.objects.create_user(
            username=clean_username,
            password=clean_password,
        )
        return user, {}

    def login(self, username, password):
        clean_username = (username or "").strip()
        clean_password = password or ""
        errors = {}

        if clean_username == "":
            errors["username"] = "Username is required."
        if clean_password == "":
            errors["password"] = "Password is required."
        if errors:
            return None, errors

        user = authenticate(username=clean_username, password=clean_password)
        if user is None:
            errors["password"] = "Invalid username or password."
            return None, errors
        return user, {}
