from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView


def index(request):
    """
    Project-specific index view that can be overridden.
    """
    context = {
        "intro": "Hello world"
    }
    return render(request, "labzero/index.html", context)


@login_required
def dashboard(request):
    """
    Project-specific dashboard view that can be overridden.
    """
    return render(request, "labzero/dashboard.html")


# Custom login/logout views that force the correct templates
class LoginView(DjangoLoginView):
    """
    Custom login view that uses the labzero login template.
    """
    template_name = 'labzero/login.html'


class LogoutView(DjangoLogoutView):
    """
    Custom logout view that uses the labzero logout template.
    """
    template_name = 'labzero/logout.html'
