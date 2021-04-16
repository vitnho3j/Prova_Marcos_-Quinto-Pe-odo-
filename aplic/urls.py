from django.urls import path

from .views import IndexView, CompetidoresView, TecnicosView, TimesView, PartidasView, OrganizadoresView, CampeonatosView, ResultadosView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('competidores/', CompetidoresView.as_view(), name = 'competidores'),
    path('tecnicos/', TecnicosView.as_view(), name = 'tecnicos'),
    path('times/', TimesView.as_view(), name = 'times'),
    path('partidas/', PartidasView.as_view(), name = 'partidas'),
    path('organizadores/', OrganizadoresView.as_view(), name = 'organizadores'),
    path('campeonatos/', CampeonatosView.as_view(), name = 'campeonatos'),
    path('resultados/', ResultadosView.as_view(), name = 'resultados')
]