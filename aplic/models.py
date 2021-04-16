from django.db import models
from stdimage.models import StdImageField
import uuid



def get_file_path(_instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return filename


class Jogo(models.Model):
    OPCOES = (
        ('MOBA', 'MOBA'),
        ('FPS', 'FPS'),
        ('Battle Royale', 'Battle Royale'),
        ('Esporte', 'Esporte'),
    )
    OPCOES1 = (
        ("RIOT", "RIOT GAMES"),
        ("GARENA", "GARENA"),
        ("VALVE", "VALVE"),
        ("EPIC GAMES", "EPIC GAMES"),
        ("EA SPORTS", "EASPORTS"),
        ("PUBG CORPORATION", "PUBG CORPORATION"),
    )
    nome = models.CharField("Nome", max_length=100)
    categoria = models.CharField('Categoria', choices = OPCOES, max_length=30)
    desenvolvedor = models.CharField('Desenvolvedor', choices= OPCOES1, max_length=30)

    class Meta:
        verbose_name = "Jogo"
        verbose_name_plural = "Jogos"

    def __str__(self):
        return self.nome


class Pessoa(models.Model):
    nome = models.CharField("Nome", max_length=100)
    idade = models.IntegerField("idade")
    cpf = models.CharField("CPF", max_length=11, unique=True)
    foto = StdImageField('Foto', null=True, blank=True, upload_to=get_file_path, variations={'thumb': {'width': 480,
                                                                                                       'height': 331,
                                                                                                       'crop': True}})

    class Meta:
        abstract = True

    def __str__(self):
        return self.nome


class Time(models.Model):
    nome = models.CharField('Nome', max_length=100)
    sigla = models.CharField('Sigla', max_length=5)
    bandeira = StdImageField('Foto', null=True, blank=True, upload_to=get_file_path, variations={'thumb': {'width': 480,
                                                                                                       'height': 331,
                                                                                                       'crop': True}})

    class Meta:
        verbose_name = "Time"
        verbose_name_plural = "Times"

    def __str__(self):
        return self.nome


class Tecnico(Pessoa):
    jogo = models.ForeignKey(Jogo, null=True, on_delete=models.SET_NULL)
    time = models.ForeignKey(Time, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Técnico"
        verbose_name_plural = "Técnicos"


class Competidor(Pessoa):
    jogo = models.ForeignKey(Jogo, null=True, on_delete=models.SET_NULL)
    time = models.ForeignKey(Time, null = True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Competidor"
        verbose_name_plural = "Competidores"


class Organizador(Pessoa):

    class Meta:
        verbose_name = "Organizador"
        verbose_name_plural = "Organizadores"

    def __str__(self):
        return self.nome


class Campeonato(models.Model):
    nome = models.CharField('Nome', max_length=100)
    dataInicio = models.DateField('Data de Início')
    dataTermino = models.DateField('Data de Término')
    regras = models.TextField('Regras')
    premiacao = models.TextField('Premiação')
    organizador = models.ForeignKey(Organizador, on_delete=models.CASCADE)
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE)
    foto = StdImageField('Foto', null=True, blank=True, upload_to=get_file_path, variations={'thumb': {'width': 480,
                                                                                                       'height': 331,
                                                                                                       'crop': True}})


    class Meta:
        verbose_name = "Campeonato"
        verbose_name_plural = "Campeonatos"

    def __str__(self):
        return self.nome


class Partida(models.Model):
    nome = models.CharField('Nome', max_length=100)
    data = models.DateField('Data')
    horario = models.TimeField('Horário')
    time = models.ManyToManyField(Time, max_length=50)
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE)
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE)


    class Meta:
        verbose_name = "Partida"
        verbose_name_plural = "Partidas"

    def __str__(self):
        return self.nome

class Resultado(models.Model):
    partida = models.ForeignKey(Partida, on_delete=models.DO_NOTHING)
    data = models.DateField('Data')
    time = models.ManyToManyField(Time)
    campeonato = models.ForeignKey(Campeonato, on_delete=models.DO_NOTHING)
    jogo = models.ForeignKey(Jogo, on_delete=models.DO_NOTHING)
    vencedor = models.ForeignKey(Time, on_delete=models.DO_NOTHING, related_name='Time_content_type')
    mvp = models.ForeignKey(Competidor, on_delete=models.DO_NOTHING)
    placar = models.TextField('Placar')


    class Meta:
        verbose_name = "Resultado"
        verbose_name_plural = "Resultados"

    def __str__(self):
        return 'Resultado'
