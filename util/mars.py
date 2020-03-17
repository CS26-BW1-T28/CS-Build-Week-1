import json
import random
import math
import sys
from chambers_attr import ChambersAttr


class Chamber:
    def __init__(self, id, title, description, x, y):
        self.id = id
        self.title = title
        self.description = description
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.u_to = None
        self.d_to = None
        self.x = x
        self.y = y

    def __repr__(self):
        if self.e_to is not None:
            return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
        return f"({self.x}, {self.y})"

    def convert_to_dict(self):
        #  Populate the dictionary with object meta data
        obj_dict = {"__class__": self.__class__.__name__, "__module__": self.__module__}
        #  Populate the dictionary with object properties
        obj_dict.update(self.__dict__)
        return obj_dict

    def connect_chambers(self, connecting_chamber, direction):
        """Connect two chambers in the given n/s/e/w/u/d direction"""
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e", "u": "d", "d": "u"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", connecting_chamber.id)
        setattr(connecting_chamber, f"{reverse_dir}_to", self.id)

    def get_chamber_in_direction(self, direction):
        """Get the connecting chamber in the given n/s/e/w/u/d direction"""
        return getattr(self, f"{direction}_to")


class Mars:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.grid = None
        self.directions = ['n', 's', 'e', 'w', 'u', 'd']

    
    def build_chambers(self, size_x, size_y, listings, total_chambers):
        self.width = size_x
        self.height = size_y
        self.grid = [None] * size_y
        self.listings = listings
        self.total_chambers = total_chambers

        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x

        # Start grid point
        x = -1
        y = 0
        chamber_count = 0
        previous_chamber = None
        direction = 1
        j = 0

        while chamber_count < total_chambers:
            ch_title = self.listings[j]['title']
            ch_desc = self.listings[j]['desc']
            # self.listings.pop(j)

            if direction > 0 and x < size_x - 1:
                chamber_direction = "e"
                x += 1
            elif direction < 0 and x > 0:
                chamber_direction = "w"
                x -= 1
            else:
                # If we hit a wall, turn north and reverse direction
                chamber_direction = "n"
                y += 1
                direction *= -1
            
            chamber = Chamber(chamber_count, ch_title, ch_desc, x, y)
            # have to save this a diff way, too, somehow? 

            # this saves room to world grid somehow?
            self.grid[y][x] = chamber

            if previous_chamber is not None:
                previous_chamber.connect_chambers(chamber, chamber_direction)

            previous_chamber = chamber
            total_chambers += 1
            j += 1


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
            if chamber is None: # ITS BREAKING BECAUSE OBJECT IS EMPTY, SO [] IS EMPTY
                print('Error: no chambers!')
                break           # MIGHT BE SELF.GRID??
            json_chamber = {}
            json_chamber["model"] = 'adventure.chamber' 
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
        f = open('generated_mars.json', "w+")
        f.write(str(formatted_fixture))
        f.close()


total_chambers = 120
width = 10
height = 8
total_levels = 6
level_length = 50

mars = Mars()
ca = ChambersAttr()
listings = ca.level_generator()

# (width, height, listings, total_chambers)
m = mars.build_chambers(width, height, listings, total_chambers) 
mars.jsonify()

print(f"\nMARS\n {m}")