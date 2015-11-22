__author__ = 'Edmond'


def parse(raw_input, directions, actions):
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
    list_text = raw_input.split(" ", 3)

    if list_text[0] == "move":                  # the move command

        if len(list_text) >= 2:                 # if the command is the right length

            if list_text[1] in directions:      # if it has the right direction
                return list_text                # return a valid command
            else:
                return ['error', 'You cannot move ' + list_text[1]]    # return an in valid direction
        else:
            return ['error', 'Be more specific. Move where?']
    else:
        return ['error', 'You cannot do ' + list_text[0]]          # return an invalid command