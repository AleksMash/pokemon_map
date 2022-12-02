from django.db import models  # noqa F401


class Pokemon(models.Model):
    name = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200, default='', blank=True)
    name_jp = models.CharField(max_length=200, default='', blank=True)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(default='', blank=True)
    ancestor = models.ForeignKey("self", on_delete=models.SET_NULL, null=True,
                                 verbose_name="Из кого эволюционировал")

    def __str__(self):
        return self.name


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(default=None)
    disappeared_at = models.DateTimeField(default=None)
    level = models.IntegerField(default=100)
    health = models.IntegerField(default=100)
    strength = models.IntegerField(default=100)
    defence = models.IntegerField(default=100)
    stamina = models.IntegerField(default=100)


