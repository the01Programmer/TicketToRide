import utility
import player_classes
import small_map_classes
import pygame
import pytest


@pytest.fixture(scope="module")
def screen():
    pygame.init()
    screen = pygame.display.set_mode((1, 1))  # dummy screen
    yield screen
    pygame.quit()


@pytest.fixture
def deck(screen):
    return player_classes.deck(screen)


@pytest.fixture
def player(deck):
    return player_classes.player(deck)


@pytest.fixture
def small_map(deck):
    return small_map_classes.Map(deck.routeCards)


#utility functions tests

def test_color_number_conversion():
    for i in range(9):
        color = utility.numbertocolor(i)
        assert utility.colortonumber(color) == i


def test_score_for_length():
    assert utility.scoreforlength(1) == 1
    assert utility.scoreforlength(3) == 4
    assert utility.scoreforlength(6) == 15


#player tests

def test_player_connection(player, small_map):
    a, b = small_map.cityList[0], small_map.cityList[1]

    assert not player.checkConnection(a, b)

    player.addConnection(a, b)

    assert player.checkConnection(a, b)


def test_player_multi_connection(player, small_map):
    a, b, c = small_map.cityList[0], small_map.cityList[1], small_map.cityList[2]

    player.addConnection(a, b)
    player.addConnection(b, c)

    assert player.checkConnection(a, c)


#map tests

def test_map_created(small_map):
    assert len(small_map.cityList) > 0
    assert len(small_map.trackList) > 0


def test_tracks_touching_city(small_map):
    city = small_map.cityList[0]
    tracks = small_map.get_tracks_touching_city(city)

    assert isinstance(tracks, list)
    assert all(city in (t.city1, t.city2) for t in tracks)


#shortest route test

def test_shortest_route_exists(small_map):
    city_a = small_map.cityList[0]
    city_b = small_map.cityList[1]

    path = utility.shortest_route(small_map, city_a, city_b)

    assert isinstance(path, list)
    if path:
        total_length = sum(t.length for t in path)
        assert total_length > 0


#longest continous route test

def test_longest_route(player, small_map):
    t1, t2 = small_map.trackList[0], small_map.trackList[1]

    t1.Owner = player
    t2.Owner = player

    player.ownedTrackList.extend([t1, t2])

    length = utility.longest_route_length(player)

    assert length >= t1.length