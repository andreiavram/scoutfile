from rest_framework import serializers

from documente.models import Registru


class RegistruSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registru
        fields = [
            "centru_local", "owner", "mod_functionare", "tip_registru", "serie", "numar_inceput",
            "numar_sfarsit", "numar_curent", "valabil", "editabil", "data_inceput", "descriere",
        ]

