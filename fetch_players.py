import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anti_fantasy_football.settings')
django.setup()

from league.models import Player

def run_fetcher():
    target_teams = {
        "133794": "Beşiktaş",
        "133804": "Galatasaray",
        "133807": "Fenerbahçe",
        "133796": "Trabzonspor",
        "133797": "Samsunspor",
        "134589": "İstanbul Başakşehir",
        "135891": "Göztepe",
        "133834": "Kasimpasa",
    }

    for team_id, team_name in target_teams.items():
        url = f"https://www.thesportsdb.com/api/v1/json/3/lookup_all_players.php?id={team_id}"
        
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            players = data.get('player', [])

            if players:
                count = 0
                for p in players:
                    api_pos = p.get('strPosition', 'Midfielder')
                    if 'Goalkeeper' in api_pos: pos = 'KL'
                    elif 'Defender' in api_pos: pos = 'DF'
                    elif 'Midfielder' in api_pos: pos = 'OS'
                    else: pos = 'FV'

                    Player.objects.update_or_create(
                        name=p['strPlayer'],
                        defaults={
                            'team': team_name,
                            'position': pos,
                            'price': 0
                        }
                    )
                    count += 1
                print(f"{team_name} için {count} oyuncu başarıyla eklendi.")
            else:
                print(f"{team_name} için oyuncu listesi boş döndü.")

        except Exception as e:
            print(f"{team_name} hatası: {e}")

    print("İşlem tamamlandı! Admin panelini kontrol et.")

if __name__ == "__main__":
    run_fetcher()