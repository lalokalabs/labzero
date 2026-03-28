from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.urls import reverse

from django_umin.views import CRUDUpdateView, CRUDView

from labzero.forms import ProfileForm


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


class ProfileCRUD(CRUDView):
    model = get_user_model()
    form_class = ProfileForm
    form_template = "labzero/profile_form.html"
    htmx_enabled = True
    htmx_redirect_on_success = False
    success_message_update = "Your profile was updated successfully."

    def get_object(self, request, queryset=None, **kwargs):
        return request.user

    def get_list_url(self):
        return reverse("labzero:dashboard")

    def get_success_url(self, obj=None):
        return reverse("labzero:profile")

    def get_form_title(self, action, obj=None):
        return "Profile Settings"

    def get_breadcrumb_label(self, action, obj=None):
        return "Dashboard"

    def get_submit_label(self, action, obj=None):
        return "Save Profile"


class ProfileUpdateView(LoginRequiredMixin, CRUDUpdateView):
    def form_valid(self, form):
        response = super().form_valid(form)

        if form.password_changed:
            update_session_auth_hash(self.request, self.object)

        return response


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
