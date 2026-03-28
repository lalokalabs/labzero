from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation


class ProfileForm(forms.ModelForm):
    current_password = forms.CharField(
        label="Current password",
        required=False,
        strip=False,
        widget=forms.PasswordInput(render_value=False),
        help_text="Required only when setting a new password.",
    )
    new_password1 = forms.CharField(
        label="New password",
        required=False,
        strip=False,
        widget=forms.PasswordInput(render_value=False),
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        required=False,
        strip=False,
        widget=forms.PasswordInput(render_value=False),
    )

    class Meta:
        model = get_user_model()
        fields = ["name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.password_changed = False

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get("current_password")
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")
        password_requested = any([current_password, new_password1, new_password2])

        if not password_requested:
            return cleaned_data

        if not current_password:
            self.add_error(
                "current_password",
                "Enter your current password to set a new password.",
            )
        elif not self.instance.check_password(current_password):
            self.add_error("current_password", "Your current password is incorrect.")

        if not new_password1:
            self.add_error("new_password1", "Enter a new password.")

        if new_password1 and new_password2 and new_password1 != new_password2:
            self.add_error("new_password2", "The new passwords do not match.")

        if (
            new_password1
            and not self.errors.get("current_password")
            and not self.errors.get("new_password2")
        ):
            password_validation.validate_password(new_password1, self.instance)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get("new_password1")

        if new_password:
            user.set_password(new_password)
            self.password_changed = True

        if commit:
            user.save()

        return user
