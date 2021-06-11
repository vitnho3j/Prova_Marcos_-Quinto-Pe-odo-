from django.core.files.storage import FileSystemStorage
from django.db.models import Count
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView
from django_weasyprint import WeasyTemplateView
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from weasyprint import HTML

from .models import Competidor, Partida, Time, Organizador, Tecnico, Campeonato, Resultado, Jogo
from chartjs.views.lines import BaseLineChartView

from django.utils.translation import gettext as _
from django.utils import translation

from .forms import ContatoForm
from django.contrib import messages

from .serializers import CompetidorSerializer, TimeSerializer, JogoSerializer


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        lang = translation.get_language()
        context['competidores'] = Competidor.objects.order_by('time').all()
        context['lang'] = lang
        translation.activate(lang)
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


class TesteView(ListView):
    template_name = 'teste.html'
    model = Competidor
    paginate_by = 3
    ordering = 'nome'

    def get_context_data(self, **kwargs):
        context = super(TesteView, self).get_context_data(**kwargs)
        id = self.kwargs['id']
        context['time'] = Time.objects.filter(id=id).first
        return context


    def get_queryset(self):
        id = self.kwargs['id']
        return Competidor.objects.filter(time_id=id)


class DadosVitoriasTimesView(BaseLineChartView):
    def get_labels(self):
        labels = []
        queryset = Time.objects.order_by('id')
        for time in queryset:
            labels.append(time.nome)
        return labels

    def get_data(self):
        resultado = []
        dados = []
        queryset = Time.objects.order_by('id').annotate(total=Count('competidores'))
        for linha in queryset:
            dados.append(int(linha.total))
        resultado.append(dados)
        return resultado


class RelatorioCompetidoresView(WeasyTemplateView):
    def get(self, request, *args, **kwargs):
        competidores = Competidor.objects.order_by('nome').all()

        html_string = render_to_string('relatorio-competidores.html', {'competidores': competidores})
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        html.write_pdf(target='/tmp/relatorio-competidores.pdf')
        fs = FileSystemStorage('/tmp')

        with fs.open("relatorio-competidores.pdf") as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline: filename="relatorio-competidores.pdf"'
        return response


class ContatoView(FormView):
    template_name = 'contato.html'
    form_class = ContatoForm
    success_url = reverse_lazy('contato')

    def get_context_data(self, **kwargs):
        context = super(ContatoView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form, *args, **kwargs):
        form.send_mail()
        messages.success(self.request, _('E-mail enviado com sucessso'), extra_tags='success')
        return super(ContatoView, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, _('Falha ao enviar e-mail'), extra_tags='danger')
        return super(ContatoView, self).form_invalid(form, *args, **kwargs)


class CompetidorViewSet(viewsets.ModelViewSet):

    queryset = Competidor.objects.all().order_by('id')
    serializer_class = CompetidorSerializer


class TimeViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissions, )
    queryset = Time.objects.all().order_by('id')
    serializer_class = TimeSerializer

    @action(detail=True, methods=['get'])
    def competidores(self, request, pk=None):
        competidores = Competidor.objects.filter(time_id=pk)
        serializer = CompetidorSerializer(competidores, many=True)
        page = self.paginate_queryset(competidores)

        if page is not None:
            serializer = CompetidorSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CompetidorSerializer(competidores, many=True)
        return Response(serializer.data)


class JogoViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissions, )
    queryset = Jogo.objects.all().order_by('id')
    serializer_class = JogoSerializer

