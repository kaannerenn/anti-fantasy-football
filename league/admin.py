from django.contrib import admin
from .models import Player, UserTeam

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'current_team','anti_score')


@admin.register(UserTeam)
class UserTeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'user', 'total_team_score')

