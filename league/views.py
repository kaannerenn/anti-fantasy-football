from django.shortcuts import render
from .models import Player
from django.shortcuts import render, get_object_or_404

def player_list(request):
    players = Player.objects.all()
    return render(request, 'league/player_list.html', {'players': players})

def player_detail(request,pk):
    player = get_object_or_404(Player,pk=pk)
    return render(request, 'league/player_detail.html',{"player": player})