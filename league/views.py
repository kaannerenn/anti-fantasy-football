from django.shortcuts import render, get_object_or_404, redirect
from .models import Player
from django.contrib import messages
from .forms import KayitFormu


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
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Hesap oluşturuldu: {username}, giriş için anasayfaya yönlendiriliyorsunuz.")
            return redirect('login')
    else:
        form = KayitFormu()
    return render(request, 'league/register.html', {'form': form})