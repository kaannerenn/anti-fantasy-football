import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anti_fantasy_football.settings')
django.setup()

from league.models import Player

def simulate_stat():
    players = Player.objects.all()

    for player in players:
        player.yellow_cards = random.randint(0, 5)
        player.red_cards = random.choice([0, 0, 0, 1])
        player.own_goals = random.choice([0, 0, 0, 0, 1])
        player.missed_penalties = random.randint(0, 2)
        player.errors_leading_to_goal = random.randint(0, 3)

        if player.position == 'KL':
            player.clean_sheets = random.choice([0, 1])
        else:
            player.clean_sheets = 0

        player.save()
        print(f"{player.name} güncellendi. Puanı: {player.anti_score}")
    
    print("Tüm oyunculara puan dağıtıldı.")

if __name__ == "__main__":
    simulate_stat()