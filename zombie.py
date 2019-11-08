import sys
import os
import string

class Survivor:
    """The playable character in the game."""   
    
    def __init__(self):
        """initialize the playable character with default attributes"""
        
        self.health_points = 100
        self.melee_weapon = Item("Frying Pan")
        self.ranged_weapon = None
        self.ammo = 0
        self.backpack = []
        self.objective_items = []
        self.city = City()
        self.location = self.city.location_dict["A"]
        self.turns_left = 30

    def take_damage(self, target):
        """Method to take damage to an instance of survivor"""  
        
        self.health_points -= target.damage
        if self.health_points <= 0:
            os.system("cls")
            print("The zombie bit you! you will turn into one of them soon. Game Over!")
            input("Press [Enter] to continue")
            sys.exit()
        else:
            print("The zombie swiped at you, and you took damage!")
            print("You have", self.health_points, "Health Points left")
            
    def location_screen(self):
        """First menu that pops up when you arrive at a location"""
        
        os.system("cls")

        if self.location.zombie_count is not None:
            self.fight_screen()
        
        if self.location.objective:
            situation = "There may be a way to escape here..."
            valid_options = {"M": "[M]ove",
                             "S": "[S]earch",
                             "H": "[H]eal",
                             "I":"[I]nfo",
                             "C": "[C]heck for Escape Route"}
            
        else:
            situation = "It looks like it's safe here..."
            valid_options = {"M": "[M]ove",
                             "S": "[S]earch",
                             "H": "[H]eal",
                             "I":"[I]nfo"}
        
        os.system("cls")
        print("Current Location:", self.location.location_name)
        print("Turns Left:", self.turns_left, end="\n\n")
        print(situation)
        print(*valid_options.values(), sep="\n")
        
        option = input("\nWhat would you like to do? \n")
        option = option.upper()

        while option not in valid_options.keys():
            os.system("cls")
            print("Current Location:", self.location.location_name)
            print("Turns Left:", self.turns_left)
            print(situation)
            print("Invalid input, please enter one of the valid inputs: ")
            print(*valid_options.values(), sep="\n", end="\n\n")
            option = input("\nWhat would you like to do? \n")
            option = option.upper()

            
        if option == "H":
            self.heal_screen()
        elif option == "M":
            self.move_screen()
        elif option == "S":
            self.search_screen()
        elif option == "I":
            self.info_screen() 
        elif option == "C":
            self.escape_screen()
         
    def info_screen(self):
        """Displays character attributes that are relevant to the player"""
       
        os.system("cls")
        print("HP:", self.health_points)
        print("Bandages:", len(self.backpack))
        print("Ammo:", self.ammo)
        print("Melee Weapon:", self.melee_weapon)
        print("Ranged Weapon:", self.ranged_weapon)
        print("Objective items:")
        print(*self.objective_items, sep="\n")
            
        input("Press [Enter] to continue")
        self.location_screen()
    
    def move_screen(self):
        """Displays possible destination and city map to help player determine where to go next"""
       
        os.system("cls")
        
        valid_options = {i:self.city.location_dict[i] for i in self.location.destinations}

        city_map = """
                     #### City Map #####
                     A     B     C     D
                     |     |     |     |
                     E-----F     G-----H
                     |     |     |     |
                     I-----J-----K     L
                     |           |     |
                     M-----N-----O     P"""
                     
        print(city_map)
        print("\nHere are your possible destinations:")
        [print(i, "-", self.city.location_dict[i]) for i in self.location.destinations]
        option = input("\nWhere would you like to go?")
        option = option.upper()
        
        while option not in valid_options.keys():
            os.system("cls")
            print(city_map)
            print("\nInvalid input, here are your possible destinations:")
            [print(i, "-", self.city.location_dict[i]) for i in self.location.destinations]
            option = input("\nWhat would you like to do? \n")
            option = option.upper()
            
        self.turns_left -= 1
        if self.turns_left == 0:
            os.system("cls")
            print("You took too long to escape the city, it's now too late to escape the city...Game Over!")
            input("Press [Enter] to continue")
            sys.exit()
        else:
            self.location = self.city.location_dict[option]
            self.location_screen()
   
        
    def fight_screen(self):
        """Fight screen that pops up when player encounters a zombie"""
        
        os.system("cls")
        
        print("(¬º-°)¬", end="\n \n")
        print("A zombie is approaching you, it wants to eat your brain")
        
        
        if self.ranged_weapon is not None and self.ammo > 0:
            valid_options = {"M": "[M]elee", "R": "[R]anged"}
            print("You have the following weapons:")
            print(*valid_options.values(), sep="\n", end="\n")
            option = input("Which one do you want to use? \n")
            option = option.upper()
            while option  not in valid_options.keys():
                print("Invalid input, please enter one of the valid inputs: ")
                print(*valid_options.values(), sep="\n", end="\n")
                option = input("What would you like to do? \n")
                option = option.upper()
            if option == "R" and self.ammo > 0:
                input("Press [Enter] to continue")
                self.attack(weapon=self.ranged_weapon)
            else:
                input("Press [Enter] to continue")
                self.attack(weapon=self.melee_weapon)
        else:
            input("Press [Enter] to continue")
            self.attack(weapon=self.melee_weapon)

    def attack(self, weapon):
        """Method to attack zombie"""
        
        os.system("cls")
        
        target = self.location.zombie_count
        weapon = weapon
        
        print("(¬º-°)¬", end="\n \n")
        print("A zombie is approaching you, it wants to eat your brain")
        
        while self.health_points > 0 and target.health_points > 0:
            input("Press [Enter] to attack")
            
            if self.ammo > 0 and weapon.category == "Ranged Weapon":    
                target.health_points -= weapon.damage
                self.ammo -= 1
            
            else:
                weapon = self.melee_weapon
                target.health_points -= weapon.damage
            
            print("You attacked the zombie with your", weapon.item_name)
            self.take_damage(target)
            if weapon.category == "Ranged Weapon" and self.ammo == 0:
                print("You ran out of ammo, switching to melee weapon")

            
        if target.health_points <= 0:
            print("You killed the zombie with your", weapon.item_name)
            self.location.zombie_count = None
            input("Press [Enter] to continue")

    def search_screen(self):
        """Displays when player decides to search the location for loots"""
        
        os.system("cls")
        
        if len(self.location.loots) == 0:
            print("There is nothing useful left...")
            input("Press [Enter] to continue")
            self.location_screen()
            
        else:
            self.loot_screen()
            
    def loot_screen(self):
        """Displays the possible loot that is in the location"""
        
        valid_options = {"Z": "Return to Game"}
        valid_options.update(self.location.loots)
        [print(i, "-", valid_options[i]) for i in valid_options]
        
        option = input("What would you like to take? \n")
        option = option.upper()
            
        while option not in valid_options.keys():
            os.system("cls")
            print("Invalid input, please enter one of the valid inputs: ")
            [print(i, "-", valid_options[i]) for i in valid_options]
            option = input("What would you like to take? \n")
            option = option.upper()
            
        if option == "Z":
            self.location_screen()
            
        elif self.location.loots[option].category == "Ammo":
            self.ammo += self.location.loots.pop(option).ammo
            
        elif self.location.loots[option].category == "Consumable Item":
            self.backpack.append(self.location.loots.pop(option))
                
        elif self.location.loots[option].category == "Objective Item":
            self.objective_items.append(self.location.loots.pop(option))
                
        elif self.location.loots[option].category == "Melee Weapon":
            self.melee_weapon = self.location.loots.pop(option)
                
        elif self.location.loots[option].category == "Ranged Weapon":
            self.ranged_weapon = self.location.loots.pop(option)
                
        self.search_screen()
            
                
    def heal_screen(self):
        """method to heal the player character if there are bandages in the inventory"""
        
        os.system("cls")
        
        if self.health_points == 100:
            print("You are at full health!")
        
        elif len(self.backpack) == 0:
            print("You don't have any bandages to heal yourself")
        
        elif self.health_points + 25 > 100:
            print("You healed yourself for 25 points, and you are now at full health!")
            self.health_points = 100
            self.backpack.pop()
        
        else:
            print("You healed yourself for 25 points, you now have",
                  self.health_points+25, "Health Points left")
            self.health_points += self.backpack.pop().heal
            
        input("Press [Enter] to continue")
        self.location_screen()

    def escape_screen(self):
        """Escape menu if the player is in the location that has an escape route"""
        
        os.system("cls")
        if self.location.location_name == "Helicopter Pad" and "Heli Key" in [i.item_name for i in self.objective_items]:
            print("There's a helicopter here, you used the the Helicopter Key you found to escape the city.")
            input("Press [Enter] to continue")
            os.system("cls")
            print("Congratulations! you've escaped, and survived to live another zombie apocalypse")
            input("Press [Enter] to continue")
            sys.exit()
        elif self.location.location_name == "Marina" and "Boat Key" in [i.item_name for i in self.objective_items]:
            print("There's a boat here, you've used the Boat Key you found to escape the city.") 
            input("Press [Enter] to continue")
            os.system("cls")
            print("Congratulations! You've survived another day.")
            input("Press [Enter] to continue")
            sys.exit()
        elif self.location.location_name == "Train Station" and self.turns_left > 20:
            print("There's a trail that leads out of the city, let's hope that you can run away in time...")
            input("Press [Enter] to continue")
            os.system("cls")
            print("Congratulations! you've escaped, and survived to live another zombie apocalypse")
            input("Press [Enter] to continue")
            sys.exit()
        elif self.location.location_name == "Train Station" and self.turns_left < 20:
            print("There's a trail that leads away from the city, let's hope that you can run away in time...")
            input("Press [Enter] to continue")
            os.system("cls")
            print("Unfortunately you didn't escape soon enough to get away from the nuclear blast radius...")
            input("Press [Enter] to continue")
            sys.exit()
        else:
            print("Doesn't look like you can escape this way, try another route")
            input("Press [Enter] to continue")
            self.location_screen()
        
class Zombie:
    """Zombies that appear in the game"""
    
    def __init__(self):
        self.health_points = 100
        self.loots = []
        self.damage = 10
        self.location = None

            
class Item:
    """Item class that can be carried by the player"""
    
    def __init__(self, item_name, description=None):
        
        self.item_name = item_name
        if item_name == "Box o' Bullets":
            self.category = "Ammo"
            self.ammo = 7   
        elif item_name == "Bandage":
            self.category = "Consumable Item"
            self.description = "Use it to patch yourself"
            self.heal = 25
        elif item_name == "Gasoline":
            self.category = "Objective Item"
            self.description = "Now if I can only find a working vehicle..."
        elif item_name == "Boat Key":
            self.category = "Objective Item"
            self.description = "Can be used to start a boat..."
        elif item_name == "Frying Pan":
            self.category = "Melee Weapon"
            self.damage = 40   
        elif item_name == "Baseball Bat":
            self.category = "Melee Weapon"
            self.damage = 50   
        elif item_name == "Handgun":
            self.category = "Ranged Weapon"
            self.damage = 100   
        elif item_name == "Heli Key":
            self.category = "Objective Item"
            self.description = "Can be used to start the helicopter..." 
        else:
            self.item_name = "Junk"
            self.category = "Junk"
            self.description = "Useless item..."

    def __repr__(self):
        return repr(self.item_name)
    
    def __str__(self):
        return str(self.item_name)
        

class Location:
    """Represents the different locations that can be explored in the game"""
    
    def __init__(self, location_name, location_desc, zombie_count, objective, destinations, loots):
        self.location_name = location_name
        self.location_desc = location_desc
        self.zombie_count = zombie_count
        self.objective = objective
        self.destinations = destinations
        self.loots = loots
        
    def __repr__(self):
        return repr(self.location_name)
    
class City:
    """Group of locations that make up the city"""
    
    def __init__(self):
        self.location_map = {"A":{"location_name": "House",
                             "location_desc": "Your house",
                             "zombie_count": None,
                             "objective" : False,
                             "destinations": ["E"],
                             "loots":{"A":Item("Box o' Bullets"), "B":Item("Bandage")}},
                        "B":{"location_name": "Bait and Tackle Shop",
                             "location_desc": "The local fishing equipment store",
                             "zombie_count": None,
                             "objective" : False,
                             "destinations": ["F"],
                             "loots": {"A": Item("Boat Key")}},
                        "C":{"location_name": "Abandoned building",
                             "location_desc": "It's an abandoned building",
                             "zombie_count": Zombie(),
                             "objective" : False,
                             "destinations": ["G"],
                             "loots":{"A":Item("Bandage")}},
                        "D":{"location_name": "Marina",
                             "location_desc": "There's a boat here",
                             "zombie_count": None,
                             "objective" : True, #escape by boat here
                             "destinations": ["H"],
                             "loots":{}},
                        "E":{"location_name": "Burned Down House",
                             "location_desc": "It's a burned down house, there may be some useful things here...",
                             "zombie_count": None,
                             "objective" : False,
                             "destinations": ["A", "F", "I"],
                             "loots":{"A":Item("Bandage")}},
                        "F":{"location_name": "Clinic",
                             "location_desc": "The local clinic, there may be some useful medical supplies here...",
                             "zombie_count": Zombie(),
                             "objective" : False,
                             "destinations": ["B", "E", "J"],
                             "loots":{"A": Item("Bandage")}},
                        "G":{"location_name": "Gas Station",
                             "location_desc": "The local Gas Station",
                             "zombie_count": None,
                             "objective" : False,
                             "destinations": ["C", "H", "K"],
                             "loots":{"A":Item("Box o' Bullets"), "B": Item("Gasoline")}},
                        "H":{"location_name": "Helicopter Pad",
                             "location_desc": "There's a functional helicopter there!",
                             "zombie_count": Zombie(),
                             "objective" : True, #escape by helicopter here
                             "destinations": ["D", "G", "L"],
                             "loots":{}},
                        "I":{"location_name": "Sporting Goods Store",
                             "location_desc": "There may be something that can be used as a weapon here...",
                             "zombie_count": None,
                             "objective" : False,
                             "destinations": ["E", "J", "M"],
                             "loots":{"A": Item("Baseball Bat")}},
                        "J":{"location_name": "Hurts Rental Car",
                             "location_desc": "There may be a usable car here...",
                             "zombie_count": None,
                             "objective" : False,
                             "destinations": ["F", "I", "K"],
                             "loots":{}},
                        "K":{"location_name": "Bakery Shop",
                             "location_desc": "The local bakery store",
                             "zombie_count": None,
                             "objective" : False,
                             "destinations": ["G", "J", "O"],
                             "loots":{}},
                        "L":{"location_name": "Convenience Store",
                             "location_desc": "The local Convenience Store",
                             "zombie_count": Zombie(),
                             "objective" : False,
                             "destinations": ["H", "P"],
                             "loots":{}},
                        "M":{"location_name": "Shooting Range",
                             "location_desc": "There are probably guns and ammo here...",
                             "zombie_count": Zombie(),
                             "objective" : False,
                             "destinations": ["I", "N"],
                             "loots":{"A": Item("Handgun")}},
                        "N":{"location_name": "Townhouse",
                             "location_desc": "It looks like there's someone yelling for help!",
                             "zombie_count": Zombie(),
                             "objective" : False,
                             "destinations": ["M", "O"],
                             "loots":{"A": Item("Heli Key")}},
                        "O":{"location_name": "Dive Bar",
                             "location_desc": "It's the local dive bar",
                             "zombie_count": Zombie(),
                             "objective" : False,
                             "destinations": ["K", "N"],
                             "loots":{"A": Item("Box o' Bullets")}},
                        "P":{"location_name": "Train Station",
                             "location_desc": "There may be a way out here...",
                             "zombie_count": None,
                             "objective" : True, #escape on foot here
                             "destinations": ["L"],
                             "loots":{}}}
        self.location_dict = {i:Location(**self.location_map[i]) for i in string.ascii_uppercase[:16]}
            
        def __repr__(self):
            return repr(self.location_dict)
    
class Game:
    """Contains the initial screens to start the game"""
    
    def __init__(self):
        self.game_name = "Citizen Evil 2"

    def title_screen(self):
        """Game title screen"""
        
        os.system("cls")
        print("###############################")
        print("# (¬º-°)¬  (¬º-°)¬ (¬º-°)¬    #")
        print("#                             #")         
        print("#       Citizen Evil 2        #")
        print("#                             #")          
        print("###############################")
        print("#           -[P]lay-          #")
        print("#           -[H]elp-          #")
        print("#           -[E]xit-          #")
        print("#                             #")
        print("###############################")
        
        option = input("What would you like to do? \n")
        while option.upper() not in ["P", "H", "E"]:
            print("Please enter a valid option")
            option = input("What would you like to do? \n")
        if option.upper() == "P":
            os.system("cls")
            self.intro_screen()
            player = Survivor()
            player.location_screen()
        elif option.upper() == "H":
            self.help_screen()
        elif option.upper() == "E":
            sys.exit()
        
    def intro_screen(self):
        """Game intro screen"""
        
        print("""
            You are in Possum City, which has experienced a zombie outbreak.
            You must find a way to get out before you are eaten alive by a zombie,
            or before the nuclear strike that will destroy the city and you along with it.
            """)
        input("Press [Enter] to continue")
      
    def help_screen(self):
        """Game help screen"""
        
        print("""
              Scavenge each location for useful items.
              There are more than one way to escape the city.
              Each time you move from one location to another, you lose a turn
              """)
        
        input("Press [Enter] to continue")
        self.title_screen()
            
#### Start the game ####
if __name__ == "__main__":
    zombie_game = Game()
    zombie_game.title_screen()
    
