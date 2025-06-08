from django.shortcuts import render
from .models import TeamMember

def team_members(request):
    team = TeamMember.objects.all()
    print(team)  # Debugging line
    return render(request, "index.html", {"team": team})
