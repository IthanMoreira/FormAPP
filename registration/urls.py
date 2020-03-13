from django.urls import path
from .views import SignUpView, ProfileUpdate, EmailUpdate

urlpatterns = [
    path('profile/', ProfileUpdate.as_view(), name="profile"),
    path('profile/email/', EmailUpdate.as_view(), name="profile_email"),
]