from django.db import models  # noqa F401


class Pokemon(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class PokemonEntity(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
