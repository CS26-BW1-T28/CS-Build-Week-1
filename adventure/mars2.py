from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import random
import json


def create_mars():
    chamber_listings = {
        0: ['Martian Surface', 'The ruddy rocky dusty terrain behind you. The entrance ahead of you, leading downwards.']
    }

    chamber_levels = ['Dirt', 'Concrete', 'Metal', 'Rock', 'Crystal']

    mars = Mars()
    mars.save()
    total_chambers = 500
    size_of_grid = 150
    length_of_each_level = 100
    number_of_levels = 5
    multiplier_of_the_level = 0

    mars.build_chambers(level=length_of_each_level, size_x=size_of_grid, size_y=size_of_grid, listings=chamber_listings)
    mars.jsonify(size_of_grid)

    chamber_listings[total_chambers + 1] = ['Martian Lair', 'Deep underground, you have stumbled upon a grisly sight... (to be continued)']

    for level in chamber_levels:
        for i in range(1, length_of_each_level + 1):
            chamber_listings[i + multiplier_of_the_level] = [f'Chamber {i + multiplier_of_the_level}: {level}', f'You are in a {level} chamber.']
        multiplier_of_the_level += length_of_each_level

    print(
        f"\nMARS\n levels: {number_of_levels},\n total chambers: {total_chambers}\n")
