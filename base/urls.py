from django.urls import path

from base.views import (CodeCompletedView, CodeView, SecureIndexView,
                        TransferView)

urlpatterns = [
    path('', SecureIndexView.as_view(), name="secure_index"),
    path('transfer/', TransferView.as_view(), name="secure_transfer"),
    path('code/', CodeView.as_view(), name="secure_code"),
    path(
        'code/completed/',
        CodeCompletedView.as_view(),
        name="secure_code_completed"
    ),
]
