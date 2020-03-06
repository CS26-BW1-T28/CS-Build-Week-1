from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import random
import json
import uuid

class Chamber(models.Model):
    id = models.IntegerField(primary_key=True, default=0)
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)
    u_to = models.IntegerField(default=0)
    d_to = models.IntegerField(default=0)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    
    def connect_chambers(self, destinationChamber, direction):
        destinationChamberID = destinationChamber.id
        try:
            destinationChamber = Chamber.objects.get(id=destinationChamberID)
        except Chamber.DoesNotExist:
            print("That chamber does not exist")
            
        else:
            if direction == "n":
                self.n_to = destinationChamberID
            elif direction == "s":
                self.s_to = destinationChamberID
            elif direction == "e":
                self.e_to = destinationChamberID
            elif direction == "w":
                self.w_to = destinationChamberID
            elif direction == "u":
                self.u_to = destinationChamberID
            elif direction == "d":
                self.d_to = destinationChamberID
            else:
                print("Invalid direction")
                return
            self.save()

    def convert_to_dict(self):
        """Returns a dictionary representation of this class including metadata such as the module and class names"""
        #  Populate the dictionary with object meta data
        obj_dict = {"__class__": self.__class__.__name__, "__module__": self.__module__}
        #  Populate the dictionary with object properties
        obj_dict.update(self.__dict__)
        if self.n_to is not None:
            obj_dict['n_to'] = self.n_to
        if self.s_to is not None:
            obj_dict['s_to'] = self.s_to
        if self.e_to is not None:
            obj_dict['e_to'] = self.e_to
        if self.w_to is not None:
            obj_dict['w_to'] = self.w_to
        if self.u_to is not None:
            obj_dict['u_to'] = self.u_to
        if self.d_to is not None:
            obj_dict['d_to'] = self.d_to
        return obj_dict

    def playerNames(self, currentPlayerID):
        return [p.user.username for p in Player.objects.filter(currentChamber=self.id) if p.id != int(currentPlayerID)]

    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentChamber=self.id) if p.id != int(currentPlayerID)]


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentChamber = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def initialize(self):
        name = 'SpaceGuy'
        if self.currentChamber == 0:
            self.currentChamber = Chamber.objects.first().id
            self.save()

    def chamber(self):
        try:
            return Chamber.objects.get(id=self.currentChamber)
        except Chamber.DoesNotExist:
            self.initialize()
            return self.chamber()

    def hasVisited(self, room):
        try:
            return PlayerVisited.objects.get(player=self, chamber=chamber)
        except PlayerVisited.DoesNotExist:
            return False
    print(Chamber)


class PlayerVisited(models.Model):
    pass


class Mars(models.Model):
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)

    def build_chambers(self, level, size_x, size_y, listings):
        self.width = size_x
        self.height = size_y
        grid = [None] * size_y
        for x in range(len(grid)):
            grid[x] = [None] * size_x

        def is_chamber_present(x_axis, y_axis):
            """Inner method for checking for the existence of a Chamber at the specified coordinates"""
            # Prevent index out of range errors
            if (x_axis >= size_x) or (y_axis >= size_y):
                return True
            if grid[y_axis][x_axis] is None:
                return False
            else:
                return True

        # Starting coordinates: (0,0) is the lower left
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
            grid[y][x] = chamber
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
            previous_chamber = chamber

        # get grid_obj(self):
        #     return [c for c in Chamber,objects.all()]

        # get_chamber(self):
        #     return [c for c in Chamber,objects.filter(id=id)]
        # grid = json.loads(mars.grid())
        #   for chamer_id in grid:
        #       chamber1 = mars.get_chamber(id)[0]

    def jsonify(self, grid_size):
        map_data = open('generated_map.txt', 'w')
        json_list = []
        grid = json.loads(Mars.grid)
        for y in range(0, grid_size):
            row_to_write = ''
            for x in range(0, grid_size):
                chamber = grid[y][x]
                if chamber is not None:
                    json_list.append(chamber.convert_to_dict())
                    row_to_write += repr(chamber)
                else:
                    row_to_write += '-----'
            map_data.write(row_to_write + '\n')
        map_data.close()

        # Save the list of dictionary-converted chambers as a .json file
        return JsonResponse('\all_chambers.json', safe=False, status=200)

        # with open('all_chambers.json', 'w') as f:
        #     json.dump(json_list, f)


@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()


