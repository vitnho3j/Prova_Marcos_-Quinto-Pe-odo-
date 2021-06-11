from django.db import models
from stdimage.models import StdImageField
import uuid
from django.utils.translation import gettext_lazy as _


def get_file_path(_instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return filename


class Jogo(models.Model):
    OPCOES = (
        ('MOBA', _('MOBA')),
        ('FPS', _('FPS')),
        ('Battle Royale', _('Battle Royale')),
        ('Esporte', _('Esporte')),
    )
    OPCOES1 = (
        ("RIOT", _("RIOT GAMES")),
        ("GARENA", _("GARENA")),
        ("VALVE", _("VALVE")),
        ("EPIC GAMES", _("EPIC GAMES")),
        ("EA SPORTS", _("EASPORTS")),
        ("PUBG CORPORATION", _("PUBG CORPORATION")),
    )
    nome = models.CharField(_("Nome"), max_length=100)
    categoria = models.CharField(_('Categoria'), choices = OPCOES, max_length=30)
    desenvolvedor = models.CharField(_('Desenvolvedor'), choices= OPCOES1, max_length=30)

    class Meta:
        verbose_name = _("Jogo")
        verbose_name_plural = _("Jogos")

    def __str__(self):
        return self.nome


class Pessoa(models.Model):
    nome = models.CharField(_("Nome"), max_length=100)
    idade = models.IntegerField(_("idade"))
    cpf = models.CharField(_("CPF"), max_length=11, unique=True)
    foto = StdImageField(_('Foto'), null=True, blank=True, upload_to=get_file_path, variations={'thumb': {'width': 480,
                                                                                                    'height': 331,
                                                                                                       'crop': True}})


    class Meta:
        abstract = True
        ordering = ['id']

    def __str__(self):
        return self.nome


class Time(models.Model):
    nome = models.CharField(_('Nome'), max_length=100)
    sigla = models.CharField(_('Sigla'), max_length=5)
    bandeira = StdImageField(_('Foto'), null=True, blank=True, upload_to=get_file_path, variations={'thumb': {'width': 480,
                                                                                                       'height': 331,
                                                                                                       'crop': True}})

    class Meta:
        verbose_name = _("Time")
        verbose_name_plural = _("Times")

    def __str__(self):
        return self.nome


class Tecnico(Pessoa):
    jogo = models.ForeignKey(Jogo, null=True, on_delete=models.SET_NULL)
    time = models.ForeignKey(Time, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['id']
        verbose_name = _("Técnico")
        verbose_name_plural = _("Técnicos")


class Competidor(Pessoa):
    jogo = models.ForeignKey(Jogo, null=True, on_delete=models.SET_NULL)
    time = models.ForeignKey(Time, null = True, on_delete=models.SET_NULL, related_name='competidores')

    class Meta:
        verbose_name = _("Competidor")
        verbose_name_plural = _("Competidores")


class Organizador(Pessoa):

    class Meta:
        verbose_name = _("Organizador")
        verbose_name_plural = _("Organizadores")

    def __str__(self):
        return self.nome


class Campeonato(models.Model):
    nome = models.CharField(_('Nome'), max_length=100)
    dataInicio = models.DateField(_('Data de Início'))
    dataTermino = models.DateField(_('Data de Término'))
    regras = models.TextField(_('Regras'))
    premiacao = models.TextField(_('Premiação'))
    organizador = models.ForeignKey(Organizador, on_delete=models.CASCADE)
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE)
    foto = StdImageField(_('Foto'), null=True, blank=True, upload_to=get_file_path, variations={'thumb': {'width': 480,
                                                                                                       'height': 331,
                                                                                                       'crop': True}})

    class Meta:
        verbose_name = _("Campeonato")
        verbose_name_plural = _("Campeonatos")

    def __str__(self):
        return self.nome


class Partida(models.Model):
    nome = models.CharField(_('Nome'), max_length=100)
    data = models.DateField(_('Data'))
    horario = models.TimeField(_('Horário'))
    time = models.ManyToManyField(Time, max_length=50)
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE)
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Partida")
        verbose_name_plural = _("Partidas")

    def __str__(self):
        return self.nome


class Resultado(models.Model):
    partida = models.ForeignKey(Partida, on_delete=models.DO_NOTHING)
    data = models.DateField(_('Data'))
    time = models.ManyToManyField(Time)
    campeonato = models.ForeignKey(Campeonato, on_delete=models.DO_NOTHING)
    jogo = models.ForeignKey(Jogo, on_delete=models.DO_NOTHING)
    vencedor = models.ForeignKey(Time, on_delete=models.DO_NOTHING, related_name='Time_content_type')
    mvp = models.ForeignKey(Competidor, on_delete=models.DO_NOTHING)
    placar = models.TextField(_('Placar'))

    class Meta:
        verbose_name = _("Resultado")
        verbose_name_plural = _("Resultados")

    def __str__(self):
        return _('Resultado')
