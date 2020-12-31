from django.db import models

from allianceauth.eveonline.models import EveCharacter, EveCorporationInfo
from eveuniverse.models import EveMoon, EveType


# Create your models here.
class Moonstuff(models.Model):

    class Meta:
        managed = False
        default_permissions = (())
        permissions = (
            ('access_moonstuff', 'Allows access to the moonstuff module'),
        )


class Resource(models.Model):
    ore = models.ForeignKey(EveType, on_delete=models.DO_NOTHING)
    quantity = models.DecimalField(max_digits=11, decimal_places=10)
    moon = models.ForeignKey(EveMoon, on_delete=models.DO_NOTHING, related_name='resources')

    class Meta:
        default_permissions = ('add',)


class Refinery(models.Model):
    structure_id = models.BigIntegerField(primary_key=True)
    evetype = models.ForeignKey(EveType, on_delete=models.DO_NOTHING)
    name = models.CharField(null=True, max_length=255)  # Might not actually need this.
    corp = models.ForeignKey(EveCorporationInfo, on_delete=models.CASCADE, related_name='refineries')

    def __str__(self):
        if self.name is None:
            return f'Unknown Structure ID{self.structure_id} ({self.evetype.name})'
        return f'{self.name}'

    class Meta:
        default_permissions = (())


class TrackingCharacter(models.Model):
    character = models.ForeignKey(EveCharacter, on_delete=models.CASCADE)
    latest_notification_id = models.BigIntegerField(null=True, default=0)
    last_notification_check = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.character.character_name}'

    class Meta:
        default_permissions = ('add',)


class Extraction(models.Model):
    start_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    decay_time = models.DateTimeField()
    moon = models.ForeignKey(EveMoon, on_delete=models.DO_NOTHING, related_name='extractions')
    refinery = models.ForeignKey(Refinery, on_delete=models.DO_NOTHING, related_name='extractions')
    corp = models.ForeignKey(EveCorporationInfo, on_delete=models.DO_NOTHING, related_name='extractions')
    jackpot = models.BooleanField(null=True)

    class Meta:
        default_permissions = (())
