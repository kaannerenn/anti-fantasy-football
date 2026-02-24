from django.shortcuts import render, get_object_or_404, redirect
from .models import Player,UserTeam
from django.contrib import messages
from .forms import KayitFormu
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def player_list(request):
    players = Player.objects.all()
    return render(request, 'league/player_list.html', {'players': players})

def player_detail(request,pk):
    player = get_object_or_404(Player,pk=pk)
    return render(request, 'league/player_detail.html',{"player": player})

def register(request):
    if request.method == 'POST':
        form = KayitFormu(request.POST)
        if form.is_valid():
            user = form.save()
            UserTeam.objects.create(
                user = user,
                team_name = f"{user.username} Kadrosu",
                # Takım adını otomatik atamak yerine soradabiliriz daha sonra (!!Hatırlatma)
            )
            login(request, user) # otomatik giriş
            messages.success(request, f"Hoş geldin {user.username}, kadron hazır. Anında oyuncu seçmeye başlayabilirsin.")
            return redirect('player_list')
    else:
        form = KayitFormu()
    return render(request, 'league/register.html', {'form': form})

@login_required
def add_to_team(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    user_team = request.user.userteam

    if player in user_team.players.all():
        messages.warning(request, f"{player.name} zaten kadronda.")

    elif user_team.players.count() >= 5:
        messages.error(request,"Kadronuz dolu maksimum 5 oyuncu seçebilirsiniz.")

    else:
        user_team.players.add(player)
        messages.success(request, f"{player.name} kadroya eklendi.")
    
    return redirect('player_list')

@login_required
def my_squad(request):
    user_team = get_object_or_404(UserTeam, user=request.user)
    players = user_team.players.all()

    return render(request, 'league/my_squad.html',
                  {
                      'user_team': user_team,
                      'players': players
                  })