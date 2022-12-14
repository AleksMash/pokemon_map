from django.db import models  # noqa F401


class Pokemon(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя")
    name_en = models.CharField(max_length=200, blank=True, verbose_name="Имя на английском")
    name_jp = models.CharField(max_length=200, blank=True, verbose_name="Иия на японском")
    image = models.ImageField(null=True, blank=True, verbose_name="Изображение")
    description = models.TextField(blank=True, verbose_name="Описание")
    ancestor = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, verbose_name="Из кого эволюционировал", related_name="descendants"
    )

    def __str__(self):
        return self.name


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name="Покемон",
                                related_name='entities')
    lat = models.FloatField(verbose_name="Широта")
    lon = models.FloatField(verbose_name="Долгота")
    appeared_at = models.DateTimeField(default=None, verbose_name="Дата и время появления")
    disappeared_at = models.DateTimeField(default=None, verbose_name="Дата и время исчезновения")
    level = models.IntegerField(verbose_name="Уровень", blank=True, null=True)
    health = models.IntegerField(verbose_name="Здоровье", blank=True, null=True)
    strength = models.IntegerField(verbose_name="Сила", blank=True, null=True)
    defence = models.IntegerField(verbose_name="Уровень защиты", blank=True, null=True)
    stamina = models.IntegerField(verbose_name="Выносливость", blank=True, null=True)
