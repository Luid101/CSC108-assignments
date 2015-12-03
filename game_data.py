class Location:

    def __init__(self, position, visit_points, brief_description, long_description, available_moves, items,
                 is_locked=False, key="", open_text="", closed_text=""):
        '''
        Creates a new location.

        Data that could be associated with each Location object:
        a position in the world map,
        a brief description,
        a long description,
        a list of available commands/directions to move,
        items that are available in the location,
        and whether or not the location has been visited before.
        Store these as you see fit.

        This is just a suggested starter class for Location.
        You may change/add parameters and the data available for each Location class as you see fit.
  
        The only thing you must NOT change is the name of this class: Location.
        All locations in your game MUST be represented as an instance of this class.

        :param position: an integer value indicating the position of that location on the map
        :param visit_points: number of points awarded to a player on first visiting a place
        :param brief_description: a brief description of the location
        :param long_description: a long description of the location
        :param available_moves: a list of available moves eg: ['west','north','east']
        :param items: a list of 'items' eg: [pen, cheat_sheet..]
        '''

        # Default variables
        self.position = position
        self.visit_points = visit_points
        self.brief_description = brief_description
        self.long_description = long_description
        self.available_moves = available_moves
        self.items = items
        self.visited = False
        self.points_given = False

        # The locked attribute variables
        self.is_locked = is_locked
        self.key = key
        self.open_text = open_text
        self.closed_text = closed_text

    def get_brief_description(self):
        '''
        Return str brief description of location.

        eg:
        get_brief_description(self)
        "lovely"

        '''
        return self.brief_description

    def get_full_description(self):
        '''
        Return str long description of location.

        eg:
        get_full_description(self)
        "lovely"

        '''
        return self.long_description

    def get_description(self):
        """
        Return a description of the location depending on if the lactation has been visited or not

        eg:
        get_description(self)
        "lovely"

        """
        if self.visited:                                                    # if the location has been visited
            return self.brief_description + "\n" + self.show_items()        # print the short description
        else:
            self.visited = True
            return self.long_description + "\n" + self.show_items()         # else print long description

    def show_items(self):
        """
        Return a description of all the items in a location

        eg:
        show_items(self)
        "You can see shoe"

        """
        if len(self.items) > 1:
            string = "You can see "

            item_list = []
            for item in self.items:
                item_list.append(item.get_name())

            string += ", ".join(item_list)

        elif len(self.items) == 1:
            string = "You can see "

            for item in self.items:
                string += item.get_name()

        else:
            string = "You don't see anything useful"

        return string + "."

    def get_items_list(self):
        """Return a description of all the items in a location in a list"""
        if len(self.items) > 0:
            item_list = []

            for item in self.items:
                item_list.append(item.get_name())

        else:
            return False

        return item_list

    def get_item(self, item_name):
        """
        takes an item name and gets back the item if it exists else return false
        :param item_name: the name of an item
        :return: return the item if it is present and False if not
        """
        if len(self.items) > 0:                         # if there is at least one item in that location
            for element in self.items:
                if element.get_name() == item_name:
                    return element
            return False
        else:
            return False

    def available_actions(self):
        '''
        -- Suggested Method (You may remove/modify/rename this as you like) --
        Return list of the available actions in this location.
        The list of actions should depend on the items available in the location
        and the x,y position of this location on the world map.
        '''
        action_text = ""
        action_list = []

        for action in self.available_moves:
            action_text += "move " + action
            action_list.append(action_text)
            action_text = ""

        return action_list


class Item:

    def __init__(self, start, target, target_points, name, exchange_item=False, exchange_with="", exchange_accepted="",
                 exchange_rejected=""):
        '''Create item referred to by string name, with integer "start"
        being the integer identifying the item's starting location,
        the integer "target" being the item's target location, and
        integer target_points being the number of points player gets
        if item is deposited in target location.

        This is just a suggested starter class for Item.
        You may change these parameters and the data available for each Item class as you see fit.
        Consider every method in this Item class as a "suggested method":
                -- Suggested Method (You may remove/modify/rename these as you like) --

        The only thing you must NOT change is the name of this class: Item.
        All item objects in your game MUST be represented as an instance of this class.
        '''

        self.name = name
        self.start = start
        self.target = target
        self.target_points = target_points
        self.placed = False                     # if the item has been placed in its target location already
        self.exchange_item = exchange_item      # if the item is exchangeable
        self.exchange_with = exchange_with      # what the item is exchangeable with
        self.exchange_accepted = exchange_accepted  # text that will be displayed when stuff is exchanged
        self.exchange_rejected = exchange_rejected  # text that will be displayed when stuff cannot be exchanged

    def get_starting_location (self):
        '''Return int location where item is first found.'''

        return self.start

    def get_name(self):
        '''Return the str name of the item.'''

        return self.name

    def get_target_location (self):
        '''Return item's int target location where it should be deposited.'''

        return self.target

    def get_target_points (self):
        '''Return int points awarded for depositing the item in its target location.'''

        return self.target_points

    def is_exchangable(self):
        """Return if it is exchangeable"""
        return self.exchange_item

    def get_exchange_item(self):
        """ :return: if this item is exchangeable and what they can be exchanged with in a list."""
        return [self.exchange_item, self.exchange_with]

    def show_trade_text(self, PLAYER, location):
        """
        Takes a player object and see's if the player has the object in its inventory,
        If it does, then drop the object from the player's inventory and add this new object to it.
        else don't do anything and return the rejected item text.
        :param PLAYER: a player object from the Player class
        :return: a string showing if the trade was successful or not
        """
        if PLAYER.get_item(self.get_exchange_item()[1]):                # if the player has the item we need
            return [True, self.exchange_accepted]           # return that the exchange has been accepted
        else:
            return [False, self.exchange_rejected]          # return that the exchange has been rejected

    def __str__(self):
        """
        :return:the string representation of the item
        """
        string = "name {0}, start_area {1}, target_area {2}, target_points {3}".format(self.get_name(),
                                                                                      self.get_starting_location(),
                                                                                      self.get_target_location(),
                                                                                      self.get_target_points())
        return string


class World:

    def __init__(self, mapdata="map.txt", locdata="locations.txt", itemdata="items.txt"):
        '''
        Creates a new World object, with a map, and data about every location and item in this game world.

        You may ADD parameters/attributes/methods to this class as you see fit.
        BUT DO NOT RENAME OR REMOVE ANY EXISTING METHODS/ATTRIBUTES.

        :param mapdata: name of text file containing map data in grid format (integers represent each location, separated by space)
                        map text file MUST be in this format.
                        E.g.
                        1 -1 3
                        4 5 6
                        Where each number represents a different location, and -1 represents an invalid, inaccessible space.
        :param locdata: name of text file containing location data (format left up to you)
        :param itemdata: name of text file containing item data (format left up to you)
        :return:
        '''
        self.map = self.load_map(mapdata) # The map MUST be stored in a nested list as described in the docstring for load_map() below
        self.items = self.load_items(itemdata) # This data must be stored somewhere. Up to you how you choose to do it...
        self.locations = self.load_locations(locdata) # This data must be stored somewhere. Up to you how you choose to do it...

    def load_map(self, filename):
        '''
        THIS FUNCTION MUST NOT BE RENAMED OR REMOVED.
        Store map from filename (map.txt) in the variable "self.map" as a nested list of integers like so:
            1 2 5
            3 -1 4
        becomes [[1,2,5], [3,-1,4]]
        RETURN THIS NEW NESTED LIST.
        :param filename: string that gives name of text file in which map data is located
        :return: return nested list of integers representing map of game world as specified above

        >>> my_world = World()
        >>> my_world.map
        [[-1, -1, -1], [-1, 0, -1], [-1, 1, -1], [-1, 2, -1], [-1, -1, -1]]

        '''
        game_map = []
        list1 = []

        file = open(filename)
        for line in file:
            list1.append(line.strip("\n").split(" "))

        for row in list1:
            element_list = []
            for element in row:
                element_list.append(int(element))
            game_map.append(element_list)

        return game_map

    def load_items(self, filename):
        '''
        Store all items from filename (items.txt) into ... whatever you think is best.
        Make sure the Item class is used to represent each item.
        Change this docstring accordingly.


        :param filename: a file with all items and their places
        :return: a dictionary with a list of items and the location number as an index
        '''

        items = {}

        file = open(filename)

        for line in file:                                   # create a dictionary of items grouping them by...
                                                            # start_location number
            if '#' not in line:                             # allows us to have comments in the file with '#'
                item_list_original = line.strip("\n").split(".")
                item_list = item_list_original[0].split(" ", 3)        # create a list with each line

                exchange_info = item_list_original[1]

                if exchange_info != '':                                                # if there is data for exchange
                    exchange_list = item_list_original[1].strip(" ").split(",")        # get data from the original list
                else:
                    exchange_list = ["False", "", "", ""]

                item = Item(int(item_list[0]),                   # create an item object from each element in the list
                            int(item_list[1]),
                            int(item_list[2]),
                            item_list[3],
                            exchange_list[0] == "True",              # returns true if the the string there is "True"
                            exchange_list[1].strip(" "),                        # send exchange_item_name
                            exchange_list[2].strip(" "),                        # send exchange_accepted text
                            exchange_list[3].strip(" "))                        # send exchange_rejected text

                if item.get_starting_location() in items:   # put that item into the dict under its target location name
                    items[item.get_starting_location()].append(item)
                else:
                    items[item.get_starting_location()] = []
                    items[item.get_starting_location()].append(item)

        file.close()

        return items

    def get_available_directions(self, location):
        """
        look at the map and figure out available move options.

        :param location: a number indicating the name of a location in the map matrix
        :return: a dictionary with possible locations ['west','east','north']
        """
        game_map = self.map                                   # makes things easier to read
        possible_directions = []

        for row in game_map:
            for location2 in row:
                if location == location2:
                    x_axis = row.index(location)
                    y_axis = game_map.index(row)

                    # The try and catch exceptions help reduce the amount of writing needed to make the map

                    try:
                        if game_map[y_axis - 1][x_axis] != -1:    # check north
                            possible_directions.append('north')
                    except IndexError:
                        pass

                    try:
                        if game_map[y_axis + 1][x_axis] != -1:    # check south
                            possible_directions.append('south')
                    except IndexError:
                        pass

                    try:
                        if game_map[y_axis][x_axis + 1] != -1:    # check east
                            possible_directions.append('east')
                    except IndexError:
                        pass

                    try:
                        if game_map[y_axis][x_axis - 1] != -1:    # check west
                            possible_directions.append('west')
                    except IndexError:
                        pass

        return possible_directions

    def load_locations(self, filename):
        '''
        Store all locations from filename (locations.txt) as a list of location
        classes into the variable self.locations.
        Remember to keep track of the integer number representing each location.
        Make sure the Location class is used to represent each location.
        Change this docstring as needed.


        :param filename: file containing all locations and their details
        :return: a dictionary containing all location objects grouped by location name
        '''

        locations_final = {}                    # a dictionary holding the location name and location object
        locations = []                          # a list containing locations stored as lists
        file = open(filename)                   # open a file with location data stored in correct format

        s = []                                  # populate the 'locations' list
        for line in file:
            if '#' not in line:                 # allow us to put comments in the file
                if "END" in line:
                    locations.append(s)
                    s = []
                else:
                    if line == "\n":
                        pass
                    else:
                        s.append(line.strip("\n"))

        for element in locations:                   # populate the 'locations_final' list with Location...
            position = int(element[0].split(" ")[1])     # objects using data from the 'locations' list

            available_directions = self.get_available_directions(position)

            if position in self.items:          # check if a location has items, if it does, load those items...
                items = self.items[position]    # else load an empty list
            else:
                items = []

            # factor in the locked variables
            key = ""
            open_text = ""
            closed_text = ""

            if len(element) > 4:                    # check if the list is long enough
                is_locked = element[4]

                if is_locked != "True":             # if !is_locked change the locked variable to False
                    is_locked = False
                else:
                    is_locked = True
                    key = element[5]
                    open_text = element[6]
                    closed_text = element[7]
            else:
                is_locked = False

            my_location = Location( position,       # create a location object with the following data
                                    element[1],
                                    element[2],
                                    element[3],
                                    available_directions,
                                    items,
                                    is_locked, key, open_text, closed_text)     # locked variables

            if position in locations_final:   # put that location into the dict under its position
                    locations_final[position] = my_location
            else:
                locations_final[position] = []
                locations_final[position] = my_location

        file.close()

        # print(locations_final)
        return locations_final

    def get_location(self, x, y):
        '''Check if location exists at location (x,y) in world map.
        Return Location object associated with this location if it does. Else, return None.
        Remember, locations represented by the number -1 on the map should return None.
        :param x: integer x representing x-coordinate of world map
        :param y: integer y representing y-coordinate of world map
        :return: Return Location object associated with this location if it does. Else, return None.
        '''

        if y < 0 or x < 0:
            return False
        else:
            if y > len(self.map):
                return False
            else:
                if x > len(self.map[y]):
                    return False
                elif self.map[y][x] == -1:
                    return False
                else:
                    return self.locations[self.map[y][x]]

# testing
"""
my_world = World()
location = my_world.get_location(2, 2)
print(location.closed_text)
"""

"""
testing items
my_world = World()
location = my_world.get_location(1, 3)
print(location.show_items())
"""

"""
# testing get_item
my_world = World()
location = my_world.get_location(1, 2)
print(location.get_item("food"))
"""


