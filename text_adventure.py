import random
import time
import os
import pygame

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_slow(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.02)
    print()

class Game:
    def __init__(self):
        self.inventory = []
        self.current_room = "entrance"
        self.game_over = False
        self.has_key = False
        self.dragon_alive = True
        self.health = 100
        self.max_health = 100
        
        # Item descriptions for the 'look' command
        self.item_descriptions = {
            "torch": "A wooden torch that provides light in dark places. It might be useful.",
            "shield": "A sturdy metal shield that can protect you from attacks.",
            "sword": "A sharp steel sword, perfect for combat.",
            "key": "A golden key that might unlock something important.",
            "gold": "Shining gold coins and bars. Very valuable!",
            "jewels": "Sparkling precious stones of various colors.",
            "potion": "A red healing potion that can restore your health.",
            "map": "A weathered map showing the cave layout."
        }
        
        self.rooms = {
            "entrance": {
                "description": "You are at the entrance of a mysterious cave. There's a torch on the wall.",
                "exits": {"north": "main_hall"},
                "items": ["torch", "map"]
            },
            "main_hall": {
                "description": "You're in a large hall with ancient markings on the walls.",
                "exits": {"south": "entrance", "east": "treasure_room", "west": "dragon_lair", "north": "potion_room"},
                "items": ["shield"]
            },
            "treasure_room": {
                "description": "A room filled with golden treasures! But the door is locked...",
                "exits": {"west": "main_hall"},
                "items": ["gold", "jewels"],
                "locked": True
            },
            "dragon_lair": {
                "description": "A massive cave with bones scattered around. A dragon sleeps here!",
                "exits": {"east": "main_hall"},
                "items": ["key", "sword"]
            },
            "potion_room": {
                "description": "A small chamber with shelves full of mysterious bottles.",
                "exits": {"south": "main_hall"},
                "items": ["potion"]
            }
        }

    def show_status(self):
        clear_screen()
        print("\n" + "="*50)
        room = self.rooms[self.current_room]
        print_slow(f"\nYou are in: {self.current_room.replace('_', ' ').title()}")
        print_slow(room["description"])
        print_slow(f"\nHealth: {self.health}/{self.max_health}")
        
        if room.get("items"):
            print_slow("\nYou see:")
            for item in room["items"]:
                print_slow(f"- {item}")
        
        print_slow("\nPossible exits:")
        for exit in room["exits"]:
            print_slow(f"- {exit}")
            
        print_slow("\nYour inventory:")
        if self.inventory:
            for item in self.inventory:
                print_slow(f"- {item}")
        else:
            print_slow("Empty")
        print("\n" + "="*50)

    def get_command(self):
        return input("\nWhat would you like to do? ").lower().split()

    def move(self, direction):
        room = self.rooms[self.current_room]
        if direction in room["exits"]:
            next_room = room["exits"][direction]
            if next_room == "treasure_room" and self.rooms["treasure_room"]["locked"]:
                if "key" in self.inventory:
                    print_slow("You use the key to unlock the door!")
                    self.rooms["treasure_room"]["locked"] = False
                else:
                    print_slow("The door is locked! You need a key.")
                    return
            self.current_room = next_room
        else:
            print_slow("You can't go that way!")

    def take(self, item):
        room = self.rooms[self.current_room]
        if item in room["items"]:
            if self.current_room == "dragon_lair" and self.dragon_alive:
                print_slow("The dragon wakes up and roars! You can't take anything while it's alive!")
                self.health -= 20
                print_slow(f"The dragon's fire hurts you! Health: {self.health}/{self.max_health}")
                if self.health <= 0:
                    print_slow("You have been defeated by the dragon!")
                    self.game_over = True
                return
            self.inventory.append(item)
            room["items"].remove(item)
            print_slow(f"You picked up the {item}!")
        else:
            print_slow("You don't see that here.")

    def drop(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            self.rooms[self.current_room]["items"].append(item)
            print_slow(f"You dropped the {item}.")
        else:
            print_slow("You don't have that item.")

    def look(self, item):
        if item in self.item_descriptions:
            if item in self.inventory or item in self.rooms[self.current_room]["items"]:
                print_slow(self.item_descriptions[item])
            else:
                print_slow("You don't see that item here.")
        else:
            print_slow("You don't see anything special about that.")

    def use(self, item):
        if item not in self.inventory:
            print_slow("You don't have that item.")
            return
            
        if item == "potion":
            if self.health < self.max_health:
                heal_amount = 50
                self.health = min(self.max_health, self.health + heal_amount)
                self.inventory.remove("potion")
                print_slow(f"You drink the potion and heal {heal_amount} health!")
                print_slow(f"Current health: {self.health}/{self.max_health}")
            else:
                print_slow("You are already at full health!")
        else:
            print_slow("You can't use that item right now.")

    def fight(self):
        if self.current_room == "dragon_lair" and self.dragon_alive:
            if "sword" in self.inventory and "shield" in self.inventory:
                print_slow("With your sword and shield, you defeat the dragon!")
                self.dragon_alive = False
            else:
                print_slow("You need both a sword and shield to fight the dragon!")
                self.health -= 30
                print_slow(f"The dragon attacks you! Health: {self.health}/{self.max_health}")
                if self.health <= 0:
                    print_slow("You have been defeated by the dragon!")
                    self.game_over = True
        else:
            print_slow("There's nothing to fight here.")

    def show_help(self):
        print_slow("\nAvailable commands:")
        print_slow("- 'go [direction]' to move (north, south, east, west)")
        print_slow("- 'take [item]' to pick up an item")
        print_slow("- 'drop [item]' to leave an item")
        print_slow("- 'look [item]' to examine an item")
        print_slow("- 'use [item]' to use an item")
        print_slow("- 'fight' to battle enemies")
        print_slow("- 'inventory' to see your items")
        print_slow("- 'help' to see this message")
        print_slow("- 'quit' to exit the game")

    def play(self):
        print_slow("\nWelcome to the Cave Adventure!")
        self.show_help()
        
        while not self.game_over:
            if self.health <= 0:
                print_slow("Game Over! You have been defeated!")
                break
                
            self.show_status()
            
            command = self.get_command()
            if not command:
                continue
                
            action = command[0]
            
            if action == "quit":
                print_slow("Thanks for playing!")
                self.game_over = True
            elif action == "go" and len(command) > 1:
                self.move(command[1])
            elif action == "take" and len(command) > 1:
                self.take(command[1])
            elif action == "drop" and len(command) > 1:
                self.drop(command[1])
            elif action == "look" and len(command) > 1:
                self.look(command[1])
            elif action == "use" and len(command) > 1:
                self.use(command[1])
            elif action == "fight":
                self.fight()
            elif action == "inventory":
                print_slow("\nYour inventory:")
                for item in self.inventory:
                    print_slow(f"- {item}")
            elif action == "help":
                self.show_help()
            else:
                print_slow("I don't understand that command.")
            
            # Check win condition
            if "gold" in self.inventory and "jewels" in self.inventory:
                print_slow("\nCongratulations! You've collected all the treasure and won the game!")
                self.game_over = True

if __name__ == "__main__":
    game = Game()
    game.play() 