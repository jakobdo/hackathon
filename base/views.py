from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext, gettext_lazy
from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  TemplateView)

from base.forms import CodeForm, TransferForm
from base.models import Deposit, DepositHistory, Transaction, User


class IndexView(TemplateView):
    template_name = 'base/index.html'


class SecureIndexView(LoginRequiredMixin, DetailView):
    model = User

    def get_object(self, queryset=None):
        return self.request.user


class CodeView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = CodeForm
    template_name = 'base/code.html'
    success_url = reverse_lazy('secure_code_completed')
    success_message = gettext_lazy(
        "Box: %(name)s was created successfully opened "
        "and %(amount)s transfered to your account"
    )

    def form_valid(self, form):
        code = form.cleaned_data['code']
        try:
            # See if we have the right code?
            deposit = Deposit.objects.get(code=code)

            # Create a deposit history entry
            # This is also used for validating that
            # the deposit can only happen once pr user!
            history = DepositHistory()
            history.deposit = deposit
            history.user = self.request.user
            history.save()

            # Create a transaction
            transaction = Transaction()
            transaction.user = self.request.user
            transaction.amount = deposit.amount
            transaction.save()

            self.object = deposit
            return super(CodeView, self).form_valid(form)
        except Deposit.DoesNotExist:
            form.add_error('code', gettext("Invalid code entered!"))
            return super(CodeView, self).form_invalid(form)
        except IntegrityError:
            form.add_error(
                'code',
                gettext("Code can only be entered once, nice try. ;)")
            )
            return super(CodeView, self).form_invalid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            name=self.object.name,
            amount=self.object.amount
        )


class CodeCompletedView(LoginRequiredMixin, TemplateView):
    template_name = 'base/completed.html'


class SignupView(CreateView):
    model = User
    fields = ['username', 'email', 'leaderboard']
    success_url = reverse_lazy('secure_index')

    def form_valid(self, form):
        self.object = form.save()
        self.object.get_start_deposit()
        login(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())


class LeaderBoardView(ListView):
    model = User
    template_name = 'base/leaderboard.html'

    def get_queryset(self):
        return self.model.objects.filter(
            role=User.Roles.STUDENT,
            leaderboard=True
        ).order_by(
            '-balance',
            'username'
        )


class TransferView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Transaction
    form_class = TransferForm
    success_url = reverse_lazy('secure_transfer')
    success_message = gettext_lazy(
        "%(amount)s$ was transfered to %(account)s"
    )

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            amount=self.object.amount,
            account=self.object.recipient
        )
