from django.urls import path
from .views import team_members

urlpatterns = [
    path("team/", team_members, name="team"),
]
