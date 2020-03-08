import random 


class ChamberAttr:
    def __init__(self):
        self.chamber_levels = ['Martian Surface', 'Dirt', 'Concrete', 'Metal', 'Crystal', 'Rock']
        
        self.level_desc = [
            {"title": "Martian Surface", "desc": "The ruddy rocky dusty terrain behind you. The entrance ahead of you, leading downwards."},
            {"title": "Martian Cave", "desc": "Endless tunnels. Each direction ends in darkness."},
            {"title": "Bunker", "desc": "Seems like a military base."},
            {"title": "Space Ship", "desc": "Arcaic alien technology never seen before. Everything creaks."},
            {"title": "Crystal Cave", "desc": "The crystals glow and shimmer so bright."},
            {"title": "Hell", "desc": "It's so hot. And I can't see the ceiling."},
        ] 
        
        self.doorways = [
            {'level': 'Martian Surface', 'title': 'the Decent', 'desc': 'A black pit in the ground, large enough to swallow a building. Where does it lead?'},
            {'level': 'Dirt', 'title': 'the Pillars', 'desc': 'Two large pillars frame a concrete ramp leading down into a bunker.'},
            {'level': 'Concrete', 'title': 'Port Hole', 'desc': 'You come to a sudden wall of metal, upon which is a round port that twists open.'},
            {'level': 'Metal', 'title': 'Damage', 'desc': 'There\'s a blast hole at the end of the room, probably from the crash.'},
            {'level': 'Crystal', 'title': 'Portal', 'desc': 'A large, warm light glistens in the middle of the chamber.'},
            {'level': 'Rock', 'title': 'Thunder Dome', 'desc': 'It\'s a fighting arena!'},
        ]
        
        self.special_chambers = [
            {'level': 'Dirt', 'title': 'Mine': 'desc': 'This chamber was recently mined. There are a few glowing red stones left in the walls.'},
            {'level': 'Concrete', 'title': 'Arms Chamber': 'desc': 'Most of the weapons are gone, but there are still a few plasma guns left.'},
            {'level': 'Concrete', 'title': 'Lab': 'desc': 'There\'s maps of planets and stars, documents in an unknown alphabet, tubes of mysterious organic materials...'},
            {'level': 'Concrete', 'title': 'Martian Lair': 'desc': 'Deep underground, you have stumbled upon a grisly sight of blood and guts. But no bodies. What happened here?'},
            {'level': 'Metal', 'title': 'Controls', 'desc': 'Looks like this is where you would fly the ship'},
            {'level': 'Metal', 'title': 'Engines', 'desc': 'Large engines and tanks. Must be where the power comes from.'},
            {'level': 'Crystal', 'title': 'Pool', 'desc': 'There is a glassy pool of a black liquid. Looks refreshing, but there are skeletons lying at the edges.'},
            {'level': 'Rock', 'title': 'Nest', 'desc': 'Eggs, everywhere.'}
        ]


    def level_generator(self):
        total_chambers = 500
        level_multiplier = 0
        level_length = 85
        chamber_listings = {
            0: ['Martian Surface', 'You take your first steps onto the surface of a new planet. The ship doors close behind you. Welcome to Mars, explorer.']}

        for level in chamber_levels:
            for i in range(1, level_length + 1):
                chamber_listings[i + level_multiplier] = [f'Level {i + level_multiplier}: {self.level_desc.level}\n{self.level_desc.desc}']
            
            level_multiplier += level_length

            chamber_listings[level_length + 1] = [f'Level {i + level_multiplier}: {self.level_desc.title}\n{self/level_desc.desc}']
