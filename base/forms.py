from django import forms
from django.utils.translation import gettext, gettext_lazy

from base.models import Transaction, User


class CodeForm(forms.Form):
    code = forms.UUIDField()


class TransferForm(forms.ModelForm):
    recipient = forms.CharField(
        label=gettext_lazy('account name'),
        max_length=150
    )

    class Meta:
        model = Transaction
        fields = ('recipient', 'amount')

    def clean_recipient(self):
        username = self.cleaned_data['recipient']
        try:
            recipient = User.objects.get(
                username=username,
                role=User.Roles.STUDENT
            )
        except User.DoesNotExist:
            raise forms.ValidationError(gettext("Invalid account name!"))
        return recipient
