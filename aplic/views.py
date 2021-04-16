from django.views.generic import TemplateView
from .models import Competidor, Partida, Time, Organizador, Tecnico, Campeonato, Resultado


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['competidores'] = Competidor.objects.order_by('time').all()
        return context


class CompetidoresView(TemplateView):
    template_name = 'competidor.html'

    def get_context_data(self, **kwargs):
        context = super(CompetidoresView, self).get_context_data(**kwargs)
        context['competidores'] = Competidor.objects.order_by('jogo', 'time').all()
        return context


class TecnicosView(TemplateView):
    template_name = 'tecnico.html'

    def get_context_data(self, **kwargs):
        context = super(TecnicosView, self).get_context_data(**kwargs)
        context['tecnicos'] = Tecnico.objects.order_by('time', 'nome').all()
        return context


class TimesView(TemplateView):
    template_name = 'times.html'

    def get_context_data(self, **kwargs):
        context = super(TimesView, self).get_context_data(**kwargs)
        context['times'] = Time.objects.order_by('nome').all()
        return context


class PartidasView(TemplateView):
    template_name = 'partidas.html'

    def get_context_data(self, **kwargs):
        context = super(PartidasView, self).get_context_data(**kwargs)
        context['partida'] = Partida.objects.order_by('campeonato').all()
        return context

class OrganizadoresView(TemplateView):
    template_name = 'organizador.html'

    def get_context_data(self, **kwargs):
        context = super(OrganizadoresView, self).get_context_data(**kwargs)
        context['organizadores'] = Organizador.objects.order_by('nome').all()
        return context

class CampeonatosView(TemplateView):
    template_name = 'campeonato.html'

    def get_context_data(self, **kwargs):
        context = super(CampeonatosView, self).get_context_data(**kwargs)
        context['campeonatos'] = Campeonato.objects.order_by('jogo', 'nome').all()
        return context


class ResultadosView(TemplateView):
    template_name = 'resultados.html'

    def get_context_data(self, **kwargs):
        context = super(ResultadosView, self).get_context_data(**kwargs)
        context['resultados'] = Resultado.objects.order_by('jogo', 'partida').all()
        return context