import json
import time
import os

def main():
    # TODO: allow them to choose from multiple JSON files?
    arr = os.listdir()
    print(arr)
    openfile = input("> ").lower().strip()
    with open(openfile) as fp:
        game = json.load(fp)
    print_instructions()
    print("You are about to play '{}'! Good luck!".format(game['__metadata__']['title']))
    print("")
    play(game)
    
    

def play(rooms):
    start_time = time.time()
    seconds = (time.time() - start_time)
    minutes = (seconds/60)
    leftoverseconds = (minutes*60 - seconds)
    # Where are we? Look in __metadata__ for the room we should start in first.
    current_place = rooms['__metadata__']['start']
    # The things the player has collected.
    stuff = ['Cell Phone; no signal or battery...']

    while True:
        # Figure out what room we're in -- current_place is a name.
        here = rooms[current_place]
        # Print the description.
        print(here["description"])

        # TODO: print any available items in the room...
        # e.g., There is a Mansion Key.
        items_here = here['items']
        print(items_here , "for the taking")
        # Is this a game-over?
        if here.get("ends_game", False):
            break

        # Allow the user to choose an exit:
        usable_exits = find_usable_exits(here, stuff)
        locked_exits = find_locked_exits(here, stuff)
        # Print out numbers for them to choose:
        for i, exit in enumerate(usable_exits):
            print("  {}. {}".format(i+1, exit['description']))
       
        # See what they typed:
        action = input("> ").lower().strip()

        # If they type any variant of quit; exit the game.
        if action in ["quit", "escape", "exit", "q"]:
            print("You quit.")
            break

        # TODO: if they type "stuff", print any items they have (check the stuff list!)
        if action in ["stuff"]:
            if len(stuff) > 0:
                print("You are carrying: " , stuff)
            else:
                print("You are not carrying anything.")
            continue
        # TODO: if they type "help", print instructions
        if action in ["help"]:
            print_instructions()
            continue
        # TODO: if they type "take", grab any items in the room.
        count = 0
        if action in ["take"]:
            for i in range(len(items_here)):
                stuff.append(items_here[i])
                items_here.remove(items_here[i])
            continue
        # TODO: if they type "drop", drop items in the room.
        if action in ["drop"]:
            drop_item = str(input("What item do you want to drop?"))
            if drop_item in stuff:
                items_here.append(drop_item)
                stuff.remove(drop_item)
            else:
                print("You cannot drop the item, because you do not have this item")
            continue
        # TODO: if they type "search", or "find", look through any exits in the room that might be hidden, and make them not hidden anymore!
        if action in ["search"]:
            for exit in here['exits']:
                if exit.get("hidden", True):
                    exit["hidden"] = False
            continue
        # Try to turn their action into an exit, by number.
        try:
            num = int(action) - 1
            selected = usable_exits[num]
            if 'required_key' not in selected:
                current_place = selected['destination']
            if 'required_key' in selected and selected['required_key'] in stuff:
                current_place = selected['destination']
            if 'required_key' in selected and selected['required_key'] not in stuff:
                print("door is locked, key is required.")
            
        except:
            print("I don't understand '{}'...".format(action))
        
    print("")
    print("")
    print("=== GAME OVER ===")
    print("minutes", int((time.time() - start_time)/60))
    print("seconds", int((time.time() - start_time)%60))
    print("It took you this much time to complete.")
def find_usable_exits(room, stuff):
    """
    Given a room, and the player's stuff, find a list of exits that they can use right now.
    That means the exits must not be hidden, and if they require a key, the player has it.
    RETURNS
     - a list of exits that are visible (not hidden) and don't require a key!
    """
    usable = []
    for exit in room['exits']:
        if exit.get("hidden", False):
            continue
        usable.append(exit)
    return usable

def find_locked_exits(room, stuff):
    """
    Given a room, and the player's stuff, find a list of exits that they can use right now.
    That means the exits must not be hidden, and if they require a key, the player has it.
    RETURNS
     - a list of exits that are visible (not hidden) and don't require a key!
    """
    locked = []
    for exit in room['exits']:
        if "required_key" in exit:
            locked.append(exit)
            continue
    return locked

def print_instructions():
    print("=== Instructions ===")
    print(" - Type a number to select an exit.")
    print(" - Type 'stuff' to see what you're carrying.")
    print(" - Type 'take' to pick up an item.")
    print(" - Type 'quit' to exit the game.")
    print(" - Type 'search' to take a deeper look at a room.")
    print("=== Instructions ===")
    print("")

if __name__ == '__main__':
    main()
