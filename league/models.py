from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    POSITIONS = [
        ('KL', 'Kaleci'),
        ('DF', 'Defans'),
        ('OS', 'Orta Saha'),
        ('FV', 'Forvet'),
    ]

    external_id = models.IntegerField(unique=True, null=True, blank=True, verbose_name="API ID")
    name = models.CharField(max_length=100, verbose_name="Oyuncu Adı")
    team = models.CharField(max_length=100, verbose_name="Takım")
    position = models.CharField(max_length=2, choices=POSITIONS, verbose_name="Mevki")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Fiyat")

    yellow_cards = models.IntegerField(default=0, verbose_name="Sarı Kart")
    red_cards = models.IntegerField(default=0, verbose_name="Kırmızı Kart")
    own_goals = models.IntegerField(default=0, verbose_name="Kendi Kalesine Gol")
    missed_penalties = models.IntegerField(default=0, verbose_name="Kaçan Penaltı")
    errors_leading_to_goal = models.IntegerField(default=0, verbose_name="Gole Sebep Olan Hata")
    clean_sheets = models.IntegerField(default=0, verbose_name="Gol yememe")

    def __str__(self):
        return f"{self.name} --- {self.team}"
    
    @property
    def anti_score(self):

        score = (self.yellow_cards * 3) + \
                (self.red_cards * 10) + \
                (self.own_goals * 15) + \
                (self.missed_penalties * 8) + \
                (self.errors_leading_to_goal * 7) - \
                (self.clean_sheets * 10)
        return score
    
class UserTeam(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Kullanıcı")
    team_name = models.CharField(max_length=100, verbose_name="Fantasy Takım Adı")
    players = models.ManyToManyField(Player, verbose_name="Kadrodaki Oyuncular")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.team_name} ({self.user.username})"

    @property
    def total_team_score(self):
        return sum(player.anti_score for player in self.players.all())