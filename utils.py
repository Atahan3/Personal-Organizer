from functools import wraps
from flask import session, redirect, request

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return redirect("/login?next=" + request.path)
        else:
            return func(*args, **kwargs)
    return wrapper