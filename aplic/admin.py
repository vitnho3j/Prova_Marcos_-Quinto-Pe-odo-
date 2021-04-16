from django.contrib import admin
from .models import Competidor, Tecnico, Partida, Jogo, Campeonato, Time, Organizador, Resultado


@admin.register(Competidor)
class CompetidorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'idade', 'jogo', 'time')


@admin.register(Tecnico)
class TecnicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'jogo')


@admin.register(Partida)
class PartidaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data', 'horario', 'campeonato')


@admin.register(Jogo)
class JogoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria')


@admin.register(Campeonato)
class CampeonatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'organizador', 'jogo')


@admin.register(Time)
class TimeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sigla')


@admin.register(Organizador)
class OrganizadorAdmin(admin.ModelAdmin):
    list_display = ['nome']


@admin.register(Resultado)
class ResultadoAdmin(admin.ModelAdmin):
    list_display = ('partida', 'campeonato', 'vencedor')