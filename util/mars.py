import json
import random


class Chamber:
    """Class to represent each Chamber (Room) in this game"""

    def __init__(self, id_num, name, description, x, y):
        """Default constructor for the instance attributes"""
        self.id = id_num
        self.name = name
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
    """Class which represents the underground labyrinthine world below the Martian environment"""

    def __init__(self):
        """Default constructor to initialize an instance of the class"""
        self.width = 0
        self.height = 0
        self.grid = None
        self.directions = ['n', 's', 'e', 'w', 'u', 'd']

    def build_chambers(self, level, size_x, size_y, listings):
        # Initialize the grid
        self.width = size_x
        self.height = size_y
        self.grid = [None] * size_y

        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x

        # Start from middle of grid (0,0)
        x = math.ceil(len(self.grid[0]) / 2)
        y = math.ceil(len(self.grid) / 2)
        chamber_count = 0
        previous_chamber = None
        node_directions = []

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

        # The following variables are to help the random generator produce something acceptable
        chamber_direction = 'd'
        descend_level = True
        level_multiplier = 1
        forbidden_directions = 's'
        previous_chamber = None

        # Each time this loop is run, another chamber is created and added to the grid
        for chamber_counter in range(len(listings)):
            chamber = Chamber(chamber_counter, listings[chamber_counter][0], listings[chamber_counter][1], x, y)
            self.grid[y][x] = chamber
            self.grid_ids[y][x] = chamber.id
            if previous_chamber is not None:
                previous_chamber.connect_chambers(chamber, chamber_direction)
                if descend_level:
                    descend_level = False

            # This case is for the second chamber which is created, because there was no previous_chamber for the first one
            elif chamber_direction == 'd':
                x += 1
                y += 1

            # Randomly assign a direction to build a chamber, if it's appropriate to do so
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
                    if 0 <= (x + test_x) < size_x:  # Ensure the chamber stays within the grid
                        if not is_chamber_present(x + test_x, y + test_y):  # Ensure no other chamber is present there
                            if chamber_direction not in forbidden_directions:  # Ensure chambers are moving in the right direction
                                invalid_direction = False

            # Only execute this block when a new level is hit
            if (chamber_counter > 0) and (chamber_counter % level) == 0:
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
            # Increment the chamber placement so that chambers aren't on top of one another
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
            # Store the current chamber so it can be connected to the next chamber on the next loop
            chamber.save()
            previous_chamber = chamber
        self.save()
        return chamber

    def jsonify(self, grid_size):
        """Method to print an ASCII map to file and all of the chambers to a JSON file"""
        # Get each chamber from the grid coordinates and write the attributes to file
        map_data = open('generated_map.txt', 'w', encoding="utf-8")
        json_list = []
        for y in range(0, grid_size):
            row_to_write = ''
            for x in range(0, grid_size):
                chamber = self.grid[y][x]
                if chamber is not None:
                    json_list.append(chamber.convert_to_dict())
                    row_to_write += repr(chamber)
                else:
                    row_to_write += '▌░░░▐'
            map_data.write(row_to_write + '\n')
        map_data.close()
        # Save the list of dictionary-converted chambers as a .json file
        with open('../fixtures/all_chambers.json', 'w') as f:
            json.dump(json_list, f)

total_chambers = 500
size_of_grid = 150
length_of_each_level = 100
number_of_levels = 5
multiplier_of_the_level = 0
chamber_listings = {
    0: ['Martian Surface', 'The ruddy rocky dusty terrain behind you. The entrance ahead of you, leading downwards.']}
chamber_levels = ['Dirt', 'Concrete', 'Metal', 'Rock', 'Crystal']
for level in chamber_levels:
    for i in range(1, length_of_each_level + 1):
        chamber_listings[i + multiplier_of_the_level] = [f'Chamber {i + multiplier_of_the_level}: {level}',
                                                         f'You are in a {level} chamber.']
    multiplier_of_the_level += length_of_each_level
chamber_listings[total_chambers + 1] = ['Martian Lair',
                                        'Deep underground, you have stumbled upon a grisly sight... (to be continued)']
mars = Mars()
mars.build_chambers(level=length_of_each_level, size_x=size_of_grid, size_y=size_of_grid, listings=chamber_listings)
mars.jsonify(size_of_grid)

print(
        f"\nMARS\n levels: {number_of_levels},\n total chambers: {total_chambers}\n")