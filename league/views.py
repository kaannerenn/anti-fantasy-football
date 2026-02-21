from django.shortcuts import render
from .models import Player

def player_list(request):
    players = Player.objects.all()
    return render(request, 'league/player_list.html', {'players': players})