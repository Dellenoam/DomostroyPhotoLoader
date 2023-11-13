from functools import wraps
from asgiref.sync import sync_to_async
from django.shortcuts import redirect


# Asynchronous function to check if the user is authenticated
@sync_to_async
def async_user_check(user):
    return user.is_authenticated


# Asynchronous decorator for mandatory login (authentication)
def async_login_required(view_func):
    @wraps(view_func)
    async def wrapped_view(request, *args, **kwargs):
        user_can_access = await async_user_check(request.user)
        if not user_can_access:
            return redirect('login')
        return await view_func(request, *args, **kwargs)

    return wrapped_view
