from game_data import World, Item, Location
from player import Player


def parse(raw_input, directions, location):
    """
    Takes in raw user input, possible directions and actions and spits out something the computer can execute
    :param raw_input: raw user input
    :return:a list of executable text

    possible commands:
    move direction, where direction is one of the possible directions

    eg:
    parse("move north",['north'],[])
    ['move', 'north']

    parse("move south west",['south'],[])
    ['move', 'south', 'west']

    """
    # directions = ['north', 'south', 'east', 'west']
    list_text = raw_input.split(" ", 1)
    tag = list_text[0]

    if tag == "inventory":                      # parse the inventory command
        return [tag, ""]

    if tag == "score":                      # parse the score command
        return [tag, ""]

    elif tag == "move" or tag == "go":          # the move command

        if len(list_text) >= 2:                 # if the command is the right length

            if list_text[1] in directions:      # if it has the right direction
                PLAYER.add_move()               # increment time
                return list_text                # return a valid command
            else:
                return ['error', 'You cannot move ' + list_text[1]]    # return an in valid direction
        else:
            return ['error', 'Be more specific. Move where?']

    elif tag == "take":                                     # the take command. dwd

        if len(list_text) >= 2:                             # if the command is the right length

            item = location.get_item(list_text[1])          # get the item in that location

            if item:                                        # if there is an item at that location

                if item.is_exchangable():                   # if the item is_exchangeable
                    return_message = item.show_trade_text(PLAYER, location)

                    if return_message[0]:  # check if the item is an exchange item and return the item needed
                        tag = "exchangeT"
                        return [tag, return_message[1], item, item.get_exchange_item()[1]]
                    else:
                        tag = "exchangeF"
                        PLAYER.add_move()                           # increment time
                        return [tag, return_message[1]]
                else:
                    PLAYER.add_move()                           # increment time
                    return [tag, item]

            else:
                return ['error', 'That item doesnt exist']  # return if the item doesn't exist

        else:
            return ['error', 'Be more specific. take what?']   # return if the command is incomplete

    elif tag == "drop":                            # the drop command

        if len(list_text) >= 2:                             # if the command is the right length

            item = PLAYER.get_item(list_text[1])          # get the item in the players inventory

            if item:                                        # if there is an item in players inventory
                PLAYER.add_move()                           # increment time
                return [tag, item]

            else:
                return ['error', 'That item doesnt exist']  # return if the item doesn't exist

        else:
            return ['error', 'Be more specific. drop what?']   # return if the command is incomplete

    else:
        return ['error', 'You cannot ' + list_text[0]]          # return an invalid command


def is_locked_move(player, original_position, move_text):
    """
    Check if a position is locked
    :param player: player object
    :param original_position: the position made before moving
    :return:string

    eg:
    is_locked_move(PLAYER, original_position, move_text)
    you cannot go in

    """

    check_location = WORLD.get_location(player.x, player.y)     # create a new location to check

    if check_location.is_locked:                                # if the location is locked and...

        if player.get_item(check_location.key) == False:        # the player does'nt have a key, then return closed_text
            player.x = original_position[0]                     # reset player locations if it can't move there
            player.y = original_position[1]
            return check_location.closed_text
        else:
            return check_location.open_text                     # if the player has a key, then return open_text

    else:
        return move_text


def do_action(World, player, location, action):
    """
    Look at an action in a specific location and modify the world/ player accordingly
    :param World: an instance of game_data.World class
    :param player: an instance of a player
    :param location: an instance of the location class
    :param action:  a possible action in that location
    :return: the result of that action

    eg:
    do_action(World, player, location, action)
    you moved south
    """

    command = parse(action, location.available_moves, location)
    tag = command[0]

    if tag == 'move' or tag == 'go':        # if it is a move command
        if command[1] == "north":
            move_text = "You move north"
            original_position = PLAYER.get_position()   # get original position
            player.move_north()
            return is_locked_move(PLAYER, original_position, move_text)

        elif command[1] == "south":
            move_text = "You move south"
            original_position = PLAYER.get_position()   # get original position
            player.move_south()
            return is_locked_move(PLAYER, original_position, move_text)

        elif command[1] == "east":
            move_text = "You move east"
            original_position = PLAYER.get_position()   # get original position
            player.move_east()
            return is_locked_move(PLAYER, original_position, move_text)

        elif command[1] == "west":
            move_text = "You move west"
            original_position = PLAYER.get_position()   # get original position
            player.move_west()
            return is_locked_move(PLAYER, original_position, move_text)

    elif tag == "error":
        return command[1] + "."

    elif tag == "take":
        PLAYER.add_item(command[1])           # add item to the inventory and remove it from the world
        location.items.remove(command[1])
        return "you took the " + command[1].get_name() + "."

    elif tag == "drop":
        location.items.append(command[1])       # add item to the world and remove it from the inventory
        PLAYER.remove_item(command[1])

        score_change = score(PLAYER, location, command[1])  # score player every time player drops the right item
        if score_change > 0:                                # in the right place
            print("You gained " + str(score_change) + " points for dropping " + command[1].get_name() + " here...")

        return "you dropped the " + command[1].get_name() + "."

    elif tag == "inventory":                    # open up the inventory
        if len(PLAYER.get_inventory()) == 2:
            return "You have " + " and ".join(PLAYER.get_inventory()) + "."
        elif len(PLAYER.get_inventory()) > 0:
            return "You have " + ", ".join(PLAYER.get_inventory()) + "."
        else:
            return "You don't have anything in your inventory."

    elif tag == "score":
        return "Your score is " + str(player.score)

    elif tag == "exchangeT":            # perform a trade

        result_text = command[1]
        location_item = command[2]
        player_item = PLAYER.get_item(command[3])

        PLAYER.remove_item(player_item)                             # drop that item from the players inventory
        PLAYER.add_item(location_item)                              # add itself to the inventory
        location.items.remove(location_item)                        # remove itself from that location

        return result_text

    elif tag == "exchangeF":            # return that a trade was not made
        return command[1]


def score(player, location, item):
    """
    checks if the player should be scored or not depending on if the player has:
    1) placed an item in the right place
    2) moved to a new location
    3) but not both at the same time

    Then gives the player points.
    This should be called anytime the player moves to a new location or drops an item

    :param player: the player object
    :param item: an item object, by default the item is False
    :param location: a location object
    :return: how many points were given

    eg:
    score(player, location, item)
    you gained 5 points fro entering this area
    your score is 10

    """

    if item:                                    # if there was an item passed through the function
        if item.target == location.position and item.placed is False:       # if the item is in its target location...
            item.placed = True                                              # and it has not been placed before
            player.score += int(item.target_points)                         # gives a player the score
            return item.target_points                                       # then return a score
        else:
            return 0                                                        # else return a score of zero

    elif location.points_given is False:              # if we are handling scoring for the location
        location.points_given = True
        player.score += int(location.visit_points)                           # gives a player the score
        return location.visit_points

    else:
        return 0


def has_won(target_items, target_location):
    """
    Checks if the user has won.
    takes the names of items in the target_items list and checks if target_location has them
    :param target_items: a list of all target items <string_list>
    :param target_location: a list of all items in the target location <string_list>
    :return: True or False depending on if the user has won or not

    eg:
    has_won(target_items, target_location)
    True

    """

    for item in target_items:                   # loop through every item in the list of target items
        if target_location.get_item(item):      # check if the item is in the target location
            pass
        else:
            return False                        # return false if it isn't
    return True                                 # return true if every item is in that location


def use_menu():
    """
    Controls user interaction on the menu
    :return:none

    eg:
    use_menu()
    menu:...

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
            print("\n" + location.get_description() + "\n")

        elif user_choice == "score":
            print("\nScore: " + str(PLAYER.score))    # display players score

        elif user_choice == "moves":
            print("\nTotal moves: " + str(PLAYER.total_moves))    # display players total moves

        elif user_choice == "back":             # exit menu
            print("menu closed")
            return

        elif user_choice == "quit":
            PLAYER.defeat = True
            return

        use_menu()                              # as long as the user did not exit return to menu

    else:
        print("Invalid menu option.")   # run itself again
        use_menu()


if __name__ == "__main__":
    WORLD = World("map.txt", "locations.txt", "items.txt")

    """
    *** CHANGE THE PLAYERS BEGINNING LOCATION HERE ***
    """
    PLAYER = Player(3, 1)    # set starting location of player; you may change the x, y coordinates here as appropriate

    menu = ["look", "score", "quit", "back", "moves"]

    while not PLAYER.victory and not PLAYER.defeat:                 # added player.defeat
        location = WORLD.get_location(PLAYER.x, PLAYER.y)           # create a new location each time

        score_change = score(PLAYER, location, "")                  # score player every time player enters new area

        if int(score_change) > 0:                                   # alert the player to point gains > 0
            print("You gained " + str(score_change) + " points for entering this area...")
            print("Your score is " + str(PLAYER.score) + "\n")                 # display score


        # ENTER CODE HERE TO PRINT LOCATION DESCRIPTION
        # depending on whether or not it's been visited before,
        #   print either full description (first time visit) or brief description (every subsequent visit)
        print(location.get_description())    # choice of full and brief description is handled inside the location class

        print("\nPossible actions: ")
        print("[menu]")
        print("[inventory]")                 # allow you to show the inventory outside of the menu
        print("take [item]")
        for action in location.available_actions():
            print(action)
        choice = input("\nEnter action: ")

        if choice == "menu":                  # if it is a menu action
            use_menu()

        else:
            # print a demarcation
            print("\n*******************************************"
                  "****************************************************************")
            print(do_action(WORLD, PLAYER, location, choice))      # do an action depending on user input

        # WINNING CONDITIONS:
        """
        ****CHANGE TARGET ITEMS AND TARGET LOCATION HERE HERE****
        """
        target_items = ["T-Card", "Cheat sheet", "Pencil"]    # target items needed
        target_location = WORLD.locations[7]    # target location that you need to put items in

        if has_won(target_items, target_location):  # check if the player has won
            PLAYER.victory = True
            print("\nCONGRATULATIONS!!! YOU PASSED!!!")
            print("It took you " + str(PLAYER.total_moves) + " moves to finish the game")
            print("Your final score is " + str(PLAYER.score))

        # LOSING CONDITIONS:
        """
        ****CHANGE NUMBER OF ALLOWED MOVES HERE****
        """
        allowed_moves = 35

        if PLAYER.total_moves > allowed_moves:
            PLAYER.defeat = True
            print("\nSORRY YOU FAILED, YOU TOOK TOO LONG AND NOW YOUR EXAM HAS BEGUN WITHOUT YOU!!!")
            print("It took you " + str(PLAYER.total_moves) + " moves ")
            print("Your final score is " + str(PLAYER.score))

        elif PLAYER.defeat:
            print("\nGOODBYE!")
            print("You quit after " + str(PLAYER.total_moves) + " moves ")
            print("Your score is " + str(PLAYER.score))








