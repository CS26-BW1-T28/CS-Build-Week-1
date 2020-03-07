from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.postgres.fields import ArrayField
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
    player = models.ForeignKey(
        'Player',
        on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        'Chamber',
        on_delete=models.CASCADE
    )



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


