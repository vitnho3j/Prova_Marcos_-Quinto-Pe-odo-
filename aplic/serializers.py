from rest_framework import serializers

from aplic.models import Competidor, Time, Jogo


class CompetidorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Competidor
        fields = (
            'nome',
            'jogo',
            'time',
        )


class TimeSerializer(serializers.ModelSerializer):
    # competidores = CompetidorSerializer(many = True, read_only=True)
    # competidores = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # competidores = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='competidores')

    class Meta:
        model = Time
        fields = (
            'nome',
            'sigla',
        )

    def validate_sigla(self, valor):
        if len(valor) < 4:
            return valor
        raise serializers.ValidationError('A Sigla inserida possúi muitas letras')


class JogoSerializer(serializers.ModelSerializer):

    bordao = serializers.SerializerMethodField()

    class Meta:
        model = Jogo
        fields = (
            'nome',
            'categoria',
            'desenvolvedor',
            'bordao',
        )

    def get_bordao(self, obj):
        return str(obj.nome).split()[0]