from django.urls import path

from base.views import SecureIndexView

urlpatterns = [
    path('', SecureIndexView.as_view(), name="secure_index"),
]
