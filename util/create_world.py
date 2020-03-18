from django.contrib.auth.models import User
from adventure.models import Player, Chamber
from chambers_attr import ChambersAttr

Chamber.objects.all().delete()

ch_outside = Chamber(level="Martian Surface", title="Outside", desc="Seas of red hills and rocks.")
ch_cave = Chamber(level="Dirt", title="Martian Cave", desc="Endless tunnels. Each direction ends in darkness.")
ch_bunker = Chamber(level="Concrete", title="Bunker", desc="Seems like a military base.")
ch_spaceship = Chamber(level="Metal", title="Space Ship", desc="Arcaic alien technology never seen before. Everything creaks.")
ch_crystal = Chamber(level="Crystal", title="Crystal Cave", desc="The crystals glow and hum.")
ch_hell = Chamber(level="Rock", title="Hell", desc="No walls. No. ceiling. Just a hot wind.")

ch_outside.save()
ch_cave.save()
ch_bunker.save()
ch_spaceship.save()
ch_crystal.save()
ch_hell.save()

# Link levels together
ch_outside.connect_chambers(ch_caves, "d")
ch_caves.connect_chambers(r_outside, "u")

ch_caves.connect_chambers(ch_bunker, "d")
ch_bunker.connect_chambers(ch_caves, "u")

ch_bunker.connect_chambers(ch_spaceship, "d")
ch_spaceship.connect_chambers(ch_bunker, "u")

ch_spaceship.connect_chambers(ch_crystal, "d")
ch_crystal.connect_chambers(ch_spaceship, "u")

ch_crystal.connect_chambers(ch_hell, "d")
ch_hell.connect_chambers(ch_crystal, "u")

players=Player.objects.all()
for p in players:
  p.current_chambers.ch_outside.id
  p.save()

