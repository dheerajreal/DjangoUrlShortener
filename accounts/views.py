from django.shortcuts import render, Http404

# Create your views here.
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from .forms import UserSignUpForm

User = get_user_model()


class SignUp(generic.CreateView):
    form_class = UserSignUpForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


class UserEmailEdit(LoginRequiredMixin, generic.UpdateView):
    model = User
    template_name = "accounts/edit_email.html"
    fields = ["email", ]

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("user_detail")


class UserProfileUpdate(LoginRequiredMixin, generic.UpdateView):
    model = User
    template_name = 'accounts/edit.html'
    fields = ["username", "first_name", "last_name", ]

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("user_detail")


@login_required
def user_profile_details(request):
    template_name = "accounts/profile.html"
    user = request.user
    context = {
        "user": user
    }
    return render(request, template_name, context)
