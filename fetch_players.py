import os
import django
import json
import time
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
from dotenv import load_dotenv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anti_fantasy_football.settings')
django.setup()
load_dotenv()

from league.models import Player

def create_oauth_json():
    oauth_data = {
        "consumer_key": os.getenv('YAHOO_CLIENT_ID'),
        "consumer_secret": os.getenv('YAHOO_CLIENT_SECRET')
    }
    with open('oauth2.json', 'w') as f:
        json.dump(oauth_data, f)

def safe_float(val):
    try:
        if val in (None, "-", "", " "): return 0.0
        return float(val)
    except: return 0.0

def clean_player_base_info(p, team_name):
    p_name = p.get("name")
    if isinstance(p_name, dict): p_name = p_name.get('full','Unknown')
    
    exclude_list = ['P', 'UTIL', 'IL', 'IL+', 'BN']
    all_pos = []
    ep = p.get('eligible_positions', [])
    if isinstance(ep, list):
        for item in ep:
            val = item.get('position') if isinstance(item, dict) else item
            if val and val.upper() not in exclude_list:
                all_pos.append(val.upper())
    
    unique_pos = sorted(list(set(all_pos)))
    return {
        "player_id": str(p['player_id']),
        "name": p_name,
        "current_team": team_name,
        "position": "/".join(unique_pos) if unique_pos else "N/A"
    }

def calculate_missed(x):
    try:
        if not x or x == "-": 
            return 0.0
            
        k = x.split('/')
        if len(k) < 2:
            return 0.0
            
        made = float(str(k[0]).replace('-', '0'))
        attempted = float(str(k[1]).replace('-', '0'))
        
        return attempted - made
    except (ValueError, IndexError, AttributeError):
        return 0.0

def run_sync():
    if not os.path.exists('oauth2.json'):
        create_oauth_json()

    sc = OAuth2(None, None, from_file='oauth2.json')
    gm = yfa.Game(sc, 'nba')
    league_id = os.getenv('YAHOO_LEAGUE_ID')
    lg = gm.to_league(f"{gm.game_id()}.l.{league_id}")

    print(f"{lg.settings()['name']} ligine bağlanıldı.")

    player_base_map = {}
    teams = lg.teams()
    for t_key, t_val in teams.items():
        t_name = t_val['name']
        team_obj = lg.to_team(t_key)
        for p in team_obj.roster():
            info = clean_player_base_info(p, t_name)
            player_base_map[info["player_id"]] = info

    try:
        fas = lg.free_agents('ALL')
        for p in fas[:300]: 
            info = clean_player_base_info(p, "Free Agent")
            player_base_map[info["player_id"]] = info
    except: pass

    player_ids = list(player_base_map.keys())
    final_data = []

    batch_size = 25
    for i in range(0, len(player_ids), batch_size):
        batch = player_ids[i:i + batch_size]
        try:
            avg_stats = lg.player_stats(batch, "average_season")
            total_stats = lg.player_stats(batch, "season")
            total_map = {str(ts['player_id']): ts for ts in total_stats}

            for s in avg_stats:
                pid = str(s.get("player_id"))
                base = player_base_map.get(pid)
                ts = total_map.get(pid, {})
                if not base: continue

                



                obj, created = Player.objects.update_or_create(
                    player_id = pid,
                    defaults ={
                        # Genel bilgiler
                    #"player_id": pid,
                    "name": base.get("name"),
                    "current_team": base.get("current_team"),
                    "position": base.get("position"),
                    # Average istatistikler
                    #"AVG_PTS": safe_float(s.get("PTS")),
                    #"AVG_REB": safe_float(s.get("REB")),
                    #"AVG_AST": safe_float(s.get("AST")),
                    #"AVG_BLK": safe_float(s.get("BLK")),
                    #"AVG_ST": safe_float(s.get("ST",s.get("STL",0))),
                    #"AVG_3PTM": safe_float(s.get("3PTM",s.get("10",0))),
                    #"AVG_TO": safe_float(s.get("TO")),
                    #"FG%": safe_float(s.get("FG%")),
                    #"FT%": safe_float(s.get("FT%")),    
                    # Total istatistikler
                    "field_goals_missed": calculate_missed(ts.get("FGM/A", "0/0")),
                    "free_throws_missed": calculate_missed(ts.get("FTM/A", "0/0")),
                    "points": safe_float(ts.get("PTS")),
                    "rebounds": safe_float(ts.get("REB")),
                    "assists": safe_float(ts.get("AST")),
                    "three_pts": safe_float(ts.get("3PTM", ts.get("10", 0))),
                    "steals": safe_float(ts.get("ST", ts.get("STL", 0))),
                    "blocks": safe_float(ts.get("BLK")),
                    "turnovers": safe_float(ts.get("TO"),)
                    }
                )
            
            print(f"İlerleme: {len(final_data)} / {len(player_ids)}")
            time.sleep(1)
        except Exception as e:
            print(f"Batch hatası ({i}): {e}")

if __name__ == "__main__":
    run_sync()