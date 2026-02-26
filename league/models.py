from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    
    player_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, verbose_name="Oyuncu Adı")
    current_team = models.CharField(max_length=100, verbose_name="Takım")
    position = models.CharField(max_length=30, verbose_name="Mevki")

    # Kötü istatistikler puan yükseltmek için 
    turnovers = models.FloatField(default=0.0, verbose_name="Top Kaybı")
    field_goals_missed = models.FloatField(default=0.0, verbose_name="Kaçan Şut")
    free_throws_missed = models.FloatField(default=0.0, verbose_name="Kaçan Serbest Atış")

    # İyi istatistikler puan düşürmek için
    points = models.FloatField(default=0.0, verbose_name="Sayı")
    rebounds = models.FloatField(default=0.0, verbose_name="Ribaund")
    assists = models.FloatField(default = 0.0, verbose_name="Asist")
    three_pts = models.FloatField(default=0.0, verbose_name="3 Sayılık Basket")
    steals = models.FloatField(default = 0.0, verbose_name="Top Çalma")
    blocks = models.FloatField(default = 0.0, verbose_name="Blok")

    def __str__(self):
        return f"{self.name} - {self.current_team}"

    @property
    def anti_score(self):
        score = (self.turnovers * 5) + \
                (self.field_goals_missed * 3) + \
                (self.free_throws_missed * 4) - \
                (self.points * 1.5) - \
                (self.rebounds * 1.5) - \
                (self.assists * 1.5) - \
                (self.three_pts * 0.5) - \
                (self.steals * 0.5) - \
                (self.blocks * 0.5)
        return round(score)
    
class UserTeam(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Kullanıcı")
    team_name = models.CharField(max_length=100, verbose_name="Fantasy Takım Adı")
    players = models.ManyToManyField(Player, blank=True, verbose_name="Oyuncular")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.team_name} ({self.user.username})"

    @property
    def total_team_score(self):
        return sum(player.anti_score for player in self.players.all())