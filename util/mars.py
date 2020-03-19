import json
import random
import math
import sys
from chambers_attr import ChambersAttr
from adventure.models import Player, Chamber

class Mars:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.grid = None
        self.directions = ["n", "s", "e", "w", "u", "d"]

    def build_chambers(self, size_x, size_y, listings, total_chambers):
        self.width = size_x
        self.height = size_y
        self.grid = [None] * size_y
        self.listings = listings
        self.total_chambers = total_chambers
        level_length = 60

        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x

        # Start grid point
        x = -1
        y = 0
        chamber_count = 0
        previous_chamber = None
        direction = 1
        j = 0

        while chamber_count <= total_chambers:
            if direction > 0 and x < size_x - 1:
                chamber_direction = "e"
                x += 1
            elif direction < 0 and x > 0:
                chamber_direction = "w"
                x -= 1
            else:
                chamber_direction = "n"
                y += 1
                direction *= -1

            ch_title = self.listings[j]["title"]
            ch_desc = self.listings[j]["desc"]
            
            chamber = Chamber(chamber_count, ch_title, ch_desc, x, y)
            # print(f"Chamber {chamber_count}\n {ch_title}: {ch_desc}\n")

            self.grid[y][x] = chamber
            chamber.save()

            if previous_chamber is not None:
                previous_chamber.connect_chambers(chamber, chamber_direction)

            if previous_chamber:
                previous_chamber.save()

            chamber.save()
            previous_chamber = chamber
            chamber_count += 1
            j += 1   

        players=Player.objects.all()
        for p in players:
            p.currentChamber = chamber[0]
            p.save()  
            

    def print_rooms(self):
        """Print the rooms in room_grid in ascii characters"""
        # Add top border
        str = "# " * ((3 + self.width * 5) // 2) + "\n"

        reverse_grid = list(self.grid)  # make a copy of the list
        reverse_grid.reverse()
        for row in reverse_grid:
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
        # Add bottom border
        str += "# " * ((3 + self.width * 5) // 2) + "\n"

        print(str)

    def jsonify(self):
        # Flatten grid of chambers
        flat_list = [item for sublist in self.grid for item in sublist]
        formatted_fixture = []
        for i, chamber in enumerate(flat_list, start=0):
            if chamber is None: # ITS BREAKING BECAUSE NO CHAMBERS ARE SAVED???
                print('Error: no chambers!')
                break          
            json_chamber = {}
            json_chamber["model"] = "adventure.chamber" 
            json_chamber["pk"] = chamber.id
            json_chamber["fields"] = {
                "title": chamber.title,
                "description": chamber.description,
                "n_to": chamber.n_to,
                "s_to": chamber.s_to,
                "e_to": chamber.e_to,
                "w_to": chamber.w_to,
                "u_to": chamber.u_to,
                "d_to": chamber.d_to,
                "x": chamber.x,
                "y": chamber.y,
            }
            formatted_fixture.append(json_chamber)
        f = open("generated_mars.json", "w+")
        f.write(str(formatted_fixture))
        f.close()


total_chambers = 360
width = 10
height = 40
total_levels = 6
level_length = 60

mars = Mars()
ca = ChambersAttr()
listings = ca.level_generator()

m = mars.build_chambers(width, height, listings, total_chambers) 
mars.jsonify()

print(f"\nMARS\n {m}")