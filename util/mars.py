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
        """Show the id of this chamber formatted with leading zeros"""
        return f"<{self.id:003}>"
        # if self.e_to is not None:
        #     return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
        # return f"({self.x}, {self.y})"

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

    
    def build_chambers(self, level, size_x, size_y, listings, total_chambers):
        self.width = size_x
        self.height = size_y
        self.grid = [None] * size_y
        self.listings = listings
        self.total_chambers = total_chambers

        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x

        # Start grid point
        x: int = 1
        y: int = 1
        chamber_count = 0
        previous_chamber = None
        chamber_directions = []
        # x = math.ceil(len(self.grid[0]) / 2)
        # y = math.ceil(len(self.grid) / 2)

        def add_chambers():
            global previous_chamber
            chamber = previous_chamber

            if chamber.n_to is None:
                print(f'Heading North.')
                chamber_directions.append('n')
            elif chamber.s_to is None:
                print(f'Heading South.')
                chamber_directions.append('s')
            elif chamber.e_to is None:
                print(f'Heading East.')
                chamber_directions.append('e')
            elif chamber.w_to is None:
                print(f'Heading West.')

            totalDirections = random.randint(1, len(chamber_directions))

            for i in range(totalDirections):
                for j in self.listings[0 + 1]:
                    ch_title = self.listings[j]['title']
                    ch_desc = self.listings[j]['desc']
                    self.listings.pop(j)

                    if chamber_directions[i] == 'n':
                        y += 1
                    if chamber_directions[i] == 's':
                        y -= 1
                    if chamber_directions[i] == 'e':
                        x += 1
                    if chamber_directions[i] == 'e':
                        x -= 1
                    
                    # Chamber( id, title, description, x, y )
                    chamber = Chamber(total_chambers, ch_title, ch_desc, x, y)

                    self.grid[x][y] = chamber

                    previous_chamber = chamber

                    total_chambers += 1

        # If self.grid is empty, jsonify() loop breaks and .json is empty
        if self.grid[0] is None and self.grid[0][0] is None:
            ch_title = self.listings[j]['title']
            ch_desc = self.listings[j]['desc']
            self.listings.pop(j)

            chamber = Chamber(total_chambers, ch_title, ch_desc, x, y)

            self.grid[x][y] = chamber

            previous_chamber = chamber
            
            total_chambers += 1

            add_chambers()
            
            chamber = chamber 

            if chamber.n_to is None:
                print(f'Heading North.')
                chamber_directions.append('n')
            elif chamber.s_to is None:
                print(f'Heading South.')
                chamber_directions.append('s')
            elif chamber.e_to is None:
                print(f'Heading East.')
                chamber_directions.append('e')
            elif chamber.w_to is None:
                print(f'Heading West.')

            totalDirections = random.randint(1, len(chamber_directions))

            for i in range(totalDirections):
                for j in self.listings[0 + 1]:
                    ch_title = self.listings[j]['title']
                    ch_desc = self.listings[j]['desc']
                    self.listings.pop(j)

                    if chamber_directions[i] == 'n':
                        y += 1
                    if chamber_directions[i] == 's':
                        y -= 1
                    if chamber_directions[i] == 'e':
                        x += 1
                    if chamber_directions[i] == 'w':
                        x -= 1
                    
                    chamber = Chamber(total_chambers, ch_title, ch_desc, x, y)

                    self.grid[x][y] = chamber

                    previous_chamber = chamber

                    total_chambers += 1

        else: 
            while total_chambers > chamber_count:
                add_chambers()

                # def add_chambers(self):
                #     global previous_chamber
                #     chamber = previous_chamber

                #     if chamber.n_to is None:
                #         print(f'Heading North.')
                #         chamber_directions.append('n')
                #     elif chamber.s_to is None:
                #         print(f'Heading South.')
                #         chamber_directions.append('s')
                #     elif chamber.e_to is None:
                #         print(f'Heading East.')
                #         chamber_directions.append('e')
                #     elif chamber.w_to is None:
                #         print(f'Heading West.')

                #     totalDirections = random.randint(1, len(chamber_directions))

                #     for i in range(totalDirections):
                #         for j in self.listings[0 + 1]:
                #             ch_title = self.listings[j]['title']
                #             ch_desc = self.listings[j]['desc']
                #             self.listings.pop(j)

                #             if chamber_directions[i] == 'n':
                #                 y += 1
                #             if chamber_directions[i] == 's':
                #                 y -= 1
                #             if chamber_directions[i] == 'e':
                #                 x += 1
                #             if chamber_directions[i] == 'e':
                #                 x -= 1
                            
                #             # Chamber( id, title, description, x, y )
                #             chamber = Chamber(total_chambers, ch_title, ch_desc, x, y)

                #             self.grid[x][y] = chamber

                #             previous_chamber = chamber

                #             total_chambers += 1




#NEXT LEVEL:
#             if (chamber_count > 0) and (chamber_count % level) == 0:
#             if self.listings[-1]:
#                 chamber_direction = 'd'
#                 descend_level = True
#                 level_multiplier += 1
#                 if level_multiplier % 5 == 0:
#                     forbidden_directions = 'w'
#                 elif level_multiplier % 4 == 0:
#                     forbidden_directions = 'w'
#                 elif level_multiplier % 3 == 0:
#                     forbidden_directions = 's'
#                 elif level_multiplier % 2 == 0:
#                     forbidden_directions = 'w'
#                 else:
#                     forbidden_directions = 's'
#                 if not is_chamber_present(x + 1, y + 1):
#                     x += 1
#                     y += 1
#                 elif not is_chamber_present(x - 1, y + 1):
#                     x -= 1
#                     y += 1
#                 elif not is_chamber_present(x + 1, y - 1):
#                     x += 1
#                     y -= 1
#                 elif not is_chamber_present(x - 1, y - 1):
#                     x -= 1
#                     y -= 1
#                 else:
#                     x = size_x
#                     y = size_y
# #####
#     def build_chambers2(self, level, size_x, size_y, listings):
#         # Each time this loop runs, another chamber is created and added to grid
#         for chamber_count in range(len(listings)):
#             chamber = Chamber(chamber_count, listings[chamber_count]['title'], listings[chamber_count]['desc'], x, y)
#             self.grid[y][x] = chamber
#             if previous_chamber is not None:
#                 previous_chamber.connect_chambers(chamber, chamber_direction)
#                 if descend_level:
#                     descend_level = False

#             # Case is for 2nd chamber created because there's no previous_chamber for the first one
#             elif chamber_direction == 'd':
#                 x += 1
#                 y += 1

#             def is_chamber_present(x_axis, y_axis):
#                 # Prevent index out of range errors
#                 if (x_axis >= size_x) or (y_axis >= size_y):
#                     return True
#                 if self.grid[y_axis][x_axis] is None:
#                     return False
#                 else:
#                     return True

#             # Randomly assign a direction to build a chamber if possible
#             invalid_direction = True
#             while invalid_direction and not descend_level:
#                 chamber_direction = ['n', 's', 'e', 'w'][random.randint(0, 3)]
#                 test_x = 0
#                 test_y = 0
#                 if chamber_direction == 'n':
#                     test_y = 1
#                 if chamber_direction == 's':
#                     test_y = -1
#                 if chamber_direction == 'e':
#                     test_x = 1
#                 if chamber_direction == 'w':
#                     test_x = -1
#                 if 0 <= (y + test_y) < size_y:  # Ensure the chamber stays within the grid
#                     if 0 <= (x + test_x) < size_x:  
#                         if not is_chamber_present(x + test_x, y + test_y):  # Ensure no other chamber is present there
#                             if chamber_direction not in forbidden_directions:  # Ensure chambers moving in the right direction
#                                 invalid_direction = False

#             # Only execute this block when a new level is hit
#             if (chamber_count > 0) and (chamber_count % level) == 0:
#                 chamber_direction = 'd'
#                 descend_level = True
#                 level_multiplier += 1
#                 if level_multiplier % 5 == 0:
#                     forbidden_directions = 'w'
#                 elif level_multiplier % 4 == 0:
#                     forbidden_directions = 'w'
#                 elif level_multiplier % 3 == 0:
#                     forbidden_directions = 's'
#                 elif level_multiplier % 2 == 0:
#                     forbidden_directions = 'w'
#                 else:
#                     forbidden_directions = 's'
#                 if not is_chamber_present(x + 1, y + 1):
#                     x += 1
#                     y += 1
#                 elif not is_chamber_present(x - 1, y + 1):
#                     x -= 1
#                     y += 1
#                 elif not is_chamber_present(x + 1, y - 1):
#                     x += 1
#                     y -= 1
#                 elif not is_chamber_present(x - 1, y - 1):
#                     x -= 1
#                     y -= 1
#                 else:
#                     x = size_x
#                     y = size_y
#             # Increment chamber placement so they're no on top of one another
#             if chamber_direction == 'n':
#                 y += 1
#             elif chamber_direction == 's':
#                 y -= 1
#             elif chamber_direction == 'e':
#                 x += 1
#             elif chamber_direction == 'w':
#                 x -= 1
#             # Ensuring the x/y coordinates do not go out of bounds
#             if x >= size_x:
#                 x = size_x - 1
#             if y >= size_y:
#                 y = size_y - 1
#             # Store the current chamber to be connected to the next chamber on the next loop
#             previous_chamber = chamber
#             chamber_count += 1 
#             return chamber

#         else:
#             while total_chambers > chamber_count:
#                 save_chamber()

        
    def jsonify(self):
        # Flatten grid of chambers
        flat_list = [item for sublist in self.grid for item in sublist]
        formatted_fixture = []
        for i, chamber in enumerate(flat_list, start=0):
            if chamber is None: # ITS BREAKING BECAUSE OBJECT IS EMPTY, SO [] IS EMPTY
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


mars = Mars()
total_chambers = 510
width = 10
height = 8

grid_size = 150
total_levels = 6
level_multiplier = 0
level_length = 50

ca = ChambersAttr()
all_levels = ca.level_generator()

# build_chambers(width, height, total_chambers, listings):
m = mars.build_chambers(level=level_length, size_x=grid_size, size_y=grid_size, listings=all_levels, total_chambers=total_chambers)
mars.jsonify()

print(f"\nMARS\n Levels: {total_levels},\n Total Chambers: {total_chambers}\n")
print(m)
