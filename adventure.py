from game_data import World, Item, Location
from player import Player


def parse(raw_input, directions, location):
    """
    Takes in raw user input, possible directions and actions and spits out something the computer can execute
    :param raw_input: raw user input
    :return:a list of executable text

    possible commands:
    move direction, where direction is one of the possible directions

    >>> parse("move north",['north'],[])
    ['move', 'north']
    >>> parse("move south west",['south'],[])
    ['move', 'south', 'west']

    """
    # directions = ['north', 'south', 'east', 'west']
    list_text = raw_input.split(" ", 1)
    tag = list_text[0]

    if tag == "inventory":                      # parse the inventory command
        return [tag, ""]

    elif tag == "move" or tag == "go":          # the move command

        if len(list_text) >= 2:                 # if the command is the right length

            if list_text[1] in directions:      # if it has the right direction
                return list_text                # return a valid command
            else:
                return ['error', 'You cannot move ' + list_text[1]]    # return an in valid direction
        else:
            return ['error', 'Be more specific. Move where?']

    elif tag == "take":                            # the take command

        if len(list_text) >= 2:                             # if the command is the right length

            item = location.get_item(list_text[1])          # get the item in that location

            if item:                                        # if there is an item at that location
                return [tag, item]

            else:
                return ['error', 'That item doesnt exist']  # return if the item doesn't exist

        else:
            return ['error', 'Be more specific. take what?']   # return if the command is incomplete

    elif tag == "drop":                            # the drop command

        if len(list_text) >= 2:                             # if the command is the right length

            item = PLAYER.get_item(list_text[1])          # get the item in the players inventory

            if item:                                        # if there is an item in players inventory
                return [tag, item]

            else:
                return ['error', 'That item doesnt exist']  # return if the item doesn't exist

        else:
            return ['error', 'Be more specific. drop what?']   # return if the command is incomplete

    else:
        return ['error', 'You cannot do ' + list_text[0]]          # return an invalid command


def do_action(World, player, location, action):
    """
    Look at an action in a specific location and modify the world/ player accordingly
    :param World: an instance of game_data.World class
    :param player: an instance of a player
    :param location: an instance of the location class
    :param action:  a possible action in that location
    :return: the result of that action
    """

    command = parse(action, location.available_moves, location)
    tag = command[0]

    if tag == 'move' or tag == 'go':        # if it is a move command
        if command[1] == "north":
            player.move_north()
            return "You move north"

        elif command[1] == "south":
            player.move_south()
            return "You move south"

        elif command[1] == "east":
            player.move_east()
            return "You move east"

        elif command[1] == "west":
            player.move_west()
            return "You move west"

    elif tag == "error":
        return command[1]

    elif tag == "take":
        PLAYER.add_item(command[1])           # add item to the inventory and remove it from the world
        location.items.remove(command[1])
        return "you took the " + command[1].get_name()

    elif tag == "drop":
        location.items.append(command[1])       # add item to the world and remove it from the inventory
        PLAYER.remove_item(command[1])
        return "you dropped the " + command[1].get_name()

    elif tag == "inventory":                    # open up the inventory
        if len(PLAYER.get_inventory()) == 2:
            return "You have " + " and ".join(PLAYER.get_inventory())
        elif len(PLAYER.get_inventory()) > 0:
            return "You have " + ", ".join(PLAYER.get_inventory())
        else:
            return "You don't have anything in your inventory"


def use_menu():
    """
    Controls user interaction on the menu
    :return:
    """

    # CALL A FUNCTION HERE TO HANDLE WHAT HAPPENS UPON USER'S CHOICE
    #    REMEMBER: the location = w.get_location(p.x, p.y) at the top of this loop will update the location if the
    #               choice the user made was just a movement, so only updating player's position is enough to change
    #               the location to the next appropriate location
    # Possibilities: a helper function do_action(WORLD, PLAYER, location, choice)
    # OR A method in World class WORLD.do_action(PLAYER, location, choice)
    # OR Check what type of action it is, then modify only player or location accordingly
    # OR Method in Player class for move or updating inventory
    # OR Method in Location class for updating location item info, or other location data
    # etc....

    print("Menu Options: \n")
    for option in menu:
        print(option)
    user_choice = input("\nChoose action: ")

    if user_choice in menu:                     # handle only choices that are in the menu

        if user_choice == "look":               # look around
            print(location.get_description())

        elif user_choice == "back":             # exit menu
            print("menu closed")
            return

        use_menu()                              # as long as the user did not exit return to menu

    else:
        print("Invalid menu option.")   # run itself again
        use_menu()


if __name__ == "__main__":
    WORLD = World("map.txt", "locations.txt", "items.txt")
    PLAYER = Player(1, 1)    # set starting location of player; you may change the x, y coordinates here as appropriate

    menu = ["look", "score", "quit", "back"]

    while not PLAYER.victory:
        location = WORLD.get_location(PLAYER.x, PLAYER.y)

        # ENTER CODE HERE TO PRINT LOCATION DESCRIPTION
        # depending on whether or not it's been visited before,
        #   print either full description (first time visit) or brief description (every subsequent visit)
        print(location.get_description())    # choice of full and brief description is handled inside the location class

        print("\nWhat to do?")
        print("[menu]")
        print("[inventory]")                     # allow you to show the inventory outside of the menu
        for action in location.available_actions():
            print(action)
        choice = input("\nEnter action: ")

        if choice == "menu":                                   # if it is a menu action
            use_menu()

        else:
            print(do_action(WORLD, PLAYER, location, choice))      # do an action depending on user input


