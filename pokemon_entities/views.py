import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime
from django.shortcuts import get_object_or_404

from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision"
    "/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832"
    "&fill=transparent"
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    current_time = localtime()
    entities = PokemonEntity.objects.filter(appeared_at__lte=current_time, disappeared_at__gt=current_time)
    for entity in entities:
        image_url = request.build_absolute_uri(location=entity.pokemon.image.url)
        add_pokemon(folium_map, entity.lat, entity.lon, image_url)
    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        image_url = request.build_absolute_uri(location=pokemon.image.url)
        pokemons_on_page.append(
            {
                "pokemon_id": pokemon.id,
                "img_url": image_url,
                "title_ru": pokemon.name,
            }
        )

    return render(
        request,
        "mainpage.html",
        context={
            "map": folium_map._repr_html_(),
            "pokemons": pokemons_on_page,
        },
    )


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, pk=pokemon_id)
    pokemon_serialized = {
        'pokemon_id': pokemon.pk,
        'title_ru': pokemon.name,
        'title_en': pokemon.name_en,
        'title_jp': pokemon.name_jp,
        'description': pokemon.description,
        'img_url': request.build_absolute_uri(location=pokemon.image.url),
    }
    ancestor: Pokemon = pokemon.ancestor
    if ancestor:
        ancestor_serialized = {
            'title_ru': ancestor.name,
            'pokemon_id': ancestor.pk,
            'img_url': request.build_absolute_uri(location=ancestor.image.url),
        }
        pokemon_serialized["previous_evolution"] = ancestor_serialized
    descendant = pokemon.descendants.all().first()
    if descendant:
        descendant_serialized = {
            'title_ru': descendant.name,
            'pokemon_id': descendant.pk,
            'img_url': request.build_absolute_uri(location=descendant.image.url),
        }
        pokemon_serialized["next_evolution"] = descendant_serialized
    current_time = localtime()
    entities = pokemon.entities.filter(appeared_at__lte=current_time, disappeared_at__gt=current_time)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in entities:
        image_url = request.build_absolute_uri(location=entity.pokemon.image.url)
        add_pokemon(folium_map, entity.lat, entity.lon, image_url)
    return render(request, "pokemon.html", context={"map": folium_map._repr_html_(), "pokemon": pokemon_json})
