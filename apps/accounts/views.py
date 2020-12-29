from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy

from . import forms


class SignupView(SuccessMessageMixin, CreateView):
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("login")
    form_class = forms.SignupForm
    success_message = "Your user was created successfully"
