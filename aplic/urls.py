from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import IndexView, CompetidoresView, TecnicosView, TimesView, PartidasView, OrganizadoresView, CampeonatosView, ResultadosView, TesteView, DadosVitoriasTimesView, RelatorioCompetidoresView, ContatoView, CompetidorViewSet, TimeViewSet, JogoViewSet

router = SimpleRouter()
router.register('competidores', CompetidorViewSet)
router.register('times', TimeViewSet)
router.register('jogos', JogoViewSet)



urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('competidores/', CompetidoresView.as_view(), name = 'competidores'),
    path('tecnicos/', TecnicosView.as_view(), name = 'tecnicos'),
    path('times/', TimesView.as_view(), name = 'times'),
    path('partidas/', PartidasView.as_view(), name = 'partidas'),
    path('organizadores/', OrganizadoresView.as_view(), name = 'organizadores'),
    path('campeonatos/', CampeonatosView.as_view(), name = 'campeonatos'),
    path('resultados/', ResultadosView.as_view(), name = 'resultados'),
    path('teste/<int:id>/', TesteView.as_view(), name="teste"),
    path('dados-vitorias-time', DadosVitoriasTimesView.as_view(), name='dados-vitorias-time'),
    path('relatorio-competidores/', RelatorioCompetidoresView.as_view(), name='relatorio-competidores'),
    path('contato/', ContatoView.as_view(), name='contato'),
]