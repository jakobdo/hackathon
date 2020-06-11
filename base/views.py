from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, TemplateView

from base.models import User


class IndexView(TemplateView):
    template_name = 'base/index.html'


class SecureIndexView(LoginRequiredMixin, DetailView):
    model = User
    #template_name = 'base/index.html'

    def get_object(self, queryset=None):
        return self.request.user
