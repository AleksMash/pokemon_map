# Generated by Django 3.1.14 on 2022-12-04 05:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0011_pokemon_ancestor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='ancestor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='descendant', to='pokemon_entities.pokemon', verbose_name='Из кого эволюционировал'),
        ),
    ]
