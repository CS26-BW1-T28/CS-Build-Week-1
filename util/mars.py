import json
import random
from chambers_attr import ChambersAttr

ca = ChambersAttr()
all_levels = ca.generator()
# print(level_lists[0:50])

class Chamber:
    """Class to represent each Chamber (Room) in this game"""

    def __init__(self, id, title, description, x, y):
        """Default constructor for the instance attributes"""
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
        """Show the id of this chamber formatted with leading zeros"""
        return f"<{self.id:003}>"

    def convert_to_dict(self):
        """Returns a dictionary representation of this class including metadata such as the module and class names"""
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

    def build_chambers(self, level, size_x, size_y, listings):
        self.width = size_x
        self.height = size_y
        self.grid = [None] * size_y
        self.listings = listings

        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x

        # Start from middle of grid (0,0)
        x = math.ceil(len(self.grid[0]) / 2)
        y = math.ceil(len(self.grid) / 2)
        chamber_count = 0
        previous_chamber = None
        chamber_directions = []

        # Prevent index out of range errors
        if (x_axis >= size_x) or (y_axis >= size_y):
            return True
        if self.grid[y_axis][x_axis] is None:
            return False
        else:
            return True

        # Starting coordinates (0,0) 
        x: int = 1
        y: int = 1

        # The following variables help the random generator produce something acceptable
        chamber_direction = 'd'
        descend_level = True
        level_multiplier = 1
        forbidden_directions = 's'
        previous_chamber = None

        # Spawn astronaut start point:
        # start_point = all_levels.chamber_listings[0]
        start_point = listings[0]
        ch_title = all_levels[0]['title']
        ch_desc = all_levels[0]['desc']
        all_levels.pop(start_point)
        chamber = Chamber(total_chambers, ch_title, ch_desc, x, y)
        # save the room
        self.grid[y][x] = chamber
        # Set previous room
        previous_chamber = chamber
        # Increment chambers
        chamber_count += 1
        # self.save()
        save_chamber()

        # Each time this loop is run, another chamber is created and added to grid
        for chamber_count in range(len(listings)):
            chamber = Chamber(chamber_count, listings[chamber_count][0], listings[chamber_count][1], x, y)
            self.grid[y][x] = chamber
            self.grid_ids[y][x] = chamber.id
            if previous_chamber is not None:
                previous_chamber.connect_chambers(chamber, chamber_direction)
                if descend_level:
                    descend_level = False

            # Case is for 2nd chamber created because there's no previous_chamber for the first one
            elif chamber_direction == 'd':
                x += 1
                y += 1

            # Randomly assign a direction to build a chamber if possible
            invalid_direction = True
            while invalid_direction and not descend_level:
                chamber_direction = ['n', 's', 'e', 'w'][random.randint(0, 3)]
                test_x = 0
                test_y = 0
                if chamber_direction == 'n':
                    test_y = 1
                if chamber_direction == 's':
                    test_y = -1
                if chamber_direction == 'e':
                    test_x = 1
                if chamber_direction == 'w':
                    test_x = -1
                if 0 <= (y + test_y) < size_y:  # Ensure the chamber stays within the grid
                    if 0 <= (x + test_x) < size_x:  
                        if not is_chamber_present(x + test_x, y + test_y):  # Ensure no other chamber is present there
                            if chamber_direction not in forbidden_directions:  # Ensure chambers moving in the right direction
                                invalid_direction = False

            # Only execute this block when a new level is hit
            if (chamber_count > 0) and (chamber_count % level) == 0:
                chamber_direction = 'd'
                descend_level = True
                level_multiplier += 1
                if level_multiplier % 5 == 0:
                    forbidden_directions = 'w'
                elif level_multiplier % 4 == 0:
                    forbidden_directions = 'w'
                elif level_multiplier % 3 == 0:
                    forbidden_directions = 's'
                elif level_multiplier % 2 == 0:
                    forbidden_directions = 'w'
                else:
                    forbidden_directions = 's'
                if not is_chamber_present(x + 1, y + 1):
                    x += 1
                    y += 1
                elif not is_chamber_present(x - 1, y + 1):
                    x -= 1
                    y += 1
                elif not is_chamber_present(x + 1, y - 1):
                    x += 1
                    y -= 1
                elif not is_chamber_present(x - 1, y - 1):
                    x -= 1
                    y -= 1
                else:
                    x = size_x
                    y = size_y
            # Increment chamber placement so they're noy on top of one another
            if chamber_direction == 'n':
                y += 1
            elif chamber_direction == 's':
                y -= 1
            elif chamber_direction == 'e':
                x += 1
            elif chamber_direction == 'w':
                x -= 1
            # Ensuring the x/y coordinates do not go out of bounds
            if x >= size_x:
                x = size_x - 1
            if y >= size_y:
                y = size_y - 1
            # Store the current chamber to be connected to the next chamber on the next loop
            chamber.save()
            previous_chamber = chamber
            chamber_count += 1 
        self.save()
        return chamber

    else:
        while total_chambers > chamber_count:
            save_chamber()

    def save_chamber(self):
        node = previous_chamber

        if node.n_to is None:
            print(f'Heading North.')
            chamber_directions.push('n')
        elif node.s_to is None:
            print(f'Heading South.')
            chamber_directions.push('s')
        elif node.e_to is None:
            print(f'Heading East.')
            chamber_directions.push('e')
        elif node.w_to is None:
            print(f'Heading West.')
            chamber_directions.push('w')
        # elif node.d_to is None:
        #     print(f'Decending 12 meters.')
        #     chamber_directions.push('d')
        # elif node.n_to is None:
        #     print(f'Acending 12 meters.')
        #     chamber_directions.push('u')

        totalDirections = random.randint(1, len(chamber_directions))

        for i in range(totalDirections):
            if all_levels.title == chamber.title
            ch_increment = all_levels[0] + 1
            ch_title - all_levels[ch_increment]['title']
            ch_desc = all_levels[ch_increment]['desc']
            all_levels.pop(ch_increment)

            if chamber_directions[i] == 'n':
                y += 1
            if chamber_directions[i] = 's':
                y -= 1
            if chamber_directions[i] == 'e':
                x += 1
            if chamber_directions[i] = 'e':
                x -= 1
            
            # Chamber(self, id, title, description, x, y)
            chamber = Chamber(total_chambers, rumTitle, rumDesc, x, y)

            self.grid[x][y] = chamber

            total_chambers += 1

    def jsonify(self):
        # Flatten grid of chambers
        flat_list = [item for sublist in self.grid for item in sublist]
        json_list = []
        for i, chamber in enumerate(flat_list, start=0):
            if chamber is None:
                continue
            json_chamber = {}
            json_chamber["model"] = 'adventure.chamber'
            json_chamber["pk"] = chamber.id
            json_chamber["fields"] = {
                "title": chamber.name,
                "description": chamber.description,
                "n_to": chamber.n_to,
                "s_to": chamber.s_to,
                "e_to": chamber.e_to,
                "w_to": chamber.w_to,
                "u_to": chamber.d_to,
                "d_to": chamber.u_to,
                "x": chamber.x,
                "y": chamber.y,
            }
            json_list.append(json_chamber)
        f = open('generated_mars.json', "w+")
        f.write(str(json_list))
        f.close()



total_chambers = 510
grid_size = 150
total_levels = 6
level_multiplier = 0
level_length = 85
width = 10
height = 8
# map: 5 x 4 || chambers: 2x2 


mars = Mars()
# width, heigh, total_chambers:
mars.build_chambers(level=level_length, size_x=grid_size, size_y=grid_size, listings=chamber_listings)
mars.jsonify()

print(f"\nMARS\n Levels: {total_levels},\n Total Chambers: Unknown\n")