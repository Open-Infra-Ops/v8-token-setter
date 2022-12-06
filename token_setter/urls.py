from django.urls import path
from token_setter.views import TokenView


urlpatterns = [
    path('token/', TokenView.as_view())
]
