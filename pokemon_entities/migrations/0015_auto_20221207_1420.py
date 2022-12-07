# Generated by Django 3.1.14 on 2022-12-07 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0014_auto_20221207_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonentity',
            name='defence',
            field=models.IntegerField(verbose_name='Уровень защиты'),
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='health',
            field=models.IntegerField(verbose_name='Здоровье'),
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='level',
            field=models.IntegerField(verbose_name='Уровень'),
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='stamina',
            field=models.IntegerField(verbose_name='Выносливость'),
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='strength',
            field=models.IntegerField(verbose_name='Сила'),
        ),
    ]