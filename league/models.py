from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    POSITIONS = [
        ('PG', 'Point Guard'),
        ('SG', 'Shooting Guard'),
        ('SF', 'Small Forward'),
        ('PF', 'Power Forward'),
        ('C', 'Center'),      
    ]

    external_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name="Oyuncu Adı")
    team = models.CharField(max_length=100, verbose_name="Takım")
    position = models.CharField(max_length=2, choices=POSITIONS, verbose_name="Mevki")

    # Kötü istatistikler puan yükseltmek için 
    turnovers = models.IntegerField(default=0, verbose_name="Top Kaybı")
    personal_fouls = models.IntegerField(default=0, verbose_name="Kişisel Faul")
    field_goals_missed = models.IntegerField(default=0, verbose_name="Kaçan Şut")
    free_throws_missed = models.IntegerField(default=0, verbose_name="Kaçan Serbest Atış")

    # İyi istatistikler puan düşürmek için
    points = models.IntegerField(default=0, verbose_name="Sayı")
    rebounds = models.IntegerField(default=0, verbose_name="Ribaund")
    assists = models.IntegerField(default = 0, verbose_name="Asist")
    three_pts = models.IntegerField(default=0, verbose_name="3 Sayılık Basket")
    steals = models.IntegerField(default = 0, verbose_name="Top Çalma")
    blocks = models.IntegerField(default=0, verbose_name="Blok")

    def __str__(self):
        return f"{self.name} - {self.team}"

    @property
    def anti_score(self):
        score = (self.turnovers * 5) + \
                (self.personal_fouls * 2) + \
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