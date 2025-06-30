from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import ProfileUpdateForm
from django.urls import reverse


@login_required
def user_profile(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'users/profile.html', context)



class UserSettings(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/update_profile.html'
    form_class = ProfileUpdateForm

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_success_url(self):
        return reverse('user:profile_home')
