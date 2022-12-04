import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime

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
    abs_uri: str = request.build_absolute_uri("/")
    pokemons = PokemonEntity.objects.filter(appeared_at__lte=localtime(), disappeared_at__gt=localtime())
    for pokemon in pokemons:
        add_pokemon(folium_map, pokemon.lat, pokemon.lon, abs_uri.rstrip("/") + pokemon.pokemon.image.url)
    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemons_on_page.append(
            {
                "pokemon_id": pokemon.id,
                "img_url": abs_uri.rstrip("/") + pokemon.image.url,
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
    try:
        pokemon = Pokemon.objects.get(pk=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound("<h1>Такой покемон не найден</h1>")
    pokemon_json = {}
    abs_uri: str = request.build_absolute_uri("/")
    pokemon_json["pokemon_id"] = pokemon.pk
    pokemon_json["title_ru"] = pokemon.name
    pokemon_json["title_en"] = pokemon.name_en
    pokemon_json["title_jp"] = pokemon.name_jp
    pokemon_json["description"] = pokemon.description
    pokemon_json["img_url"] = abs_uri.rstrip("/") + pokemon.image.url
    ancestor: Pokemon = pokemon.ancestor
    if ancestor:
        ancestor_json = {}
        ancestor_json["title_ru"] = ancestor.name
        ancestor_json["pokemon_id"] = ancestor.pk
        ancestor_json["img_url"] = abs_uri.rstrip("/") + ancestor.image.url
        pokemon_json["previous_evolution"] = ancestor_json
    descendants = pokemon.descendant.all()
    if descendants:
        descendant = descendants[0]
        descendant_json = {}
        descendant_json["title_ru"] = descendant.name
        descendant_json["pokemon_id"] = descendant.pk
        descendant_json["img_url"] = abs_uri.rstrip("/") + descendant.image.url
        pokemon_json["next_evolution"] = descendant_json
    entities = PokemonEntity.objects.filter(
        pokemon=pokemon, appeared_at__lte=localtime(), disappeared_at__gt=localtime()
    )
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in entities:
        add_pokemon(folium_map, pokemon.lat, pokemon.lon, abs_uri.rstrip("/") + pokemon.pokemon.image.url)
    return render(request, "pokemon.html", context={"map": folium_map._repr_html_(), "pokemon": pokemon_json})
