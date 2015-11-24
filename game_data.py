class Location:

    def __init__(self, position, visit_points, brief_description, long_description, available_moves, items):
        '''Creates a new location.

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

        self.position = position
        self.visit_points = visit_points
        self.brief_description = brief_description
        self.long_description = long_description
        self.available_moves = available_moves
        self.items = items
        self.visited = False
        self.points_given = False

    def get_brief_description (self):
        '''Return str brief description of location.'''
        return self.brief_description

    def get_full_description (self):
        '''Return str long description of location.'''
        return self.long_description

    def get_description(self):
        """Return a description of the location depending on if the lactation has been visited or not"""
        if self.visited:                                                    # if the location has been visited
            return self.brief_description + "\n" + self.show_items()        # print the short description
        else:
            self.visited = True
            return self.long_description + "\n" + self.show_items()         # else print long description

    def show_items(self):
        """Return a description of all the items in a location"""
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

    def __init__ (self, start, target, target_points, name):
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
                item_list = line.strip("\n").split(" ", 3)     # create a list with each line

                item = Item(int(item_list[0]),                   # create an item object from each element in the list
                            int(item_list[1]),
                            int(item_list[2]),
                            item_list[3])

                if item.get_starting_location() in items:   # put that item into the dict under its target location name
                    items[item.get_starting_location()].append(item)
                else:
                    items[item.get_starting_location()] = []
                    items[item.get_starting_location()].append(item)

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

                    if game_map[y_axis - 1][x_axis] != -1:    # check north
                        possible_directions.append('north')

                    if game_map[y_axis + 1][x_axis] != -1:    # check south
                        possible_directions.append('south')

                    if game_map[y_axis][x_axis + 1] != -1:    # check east
                        possible_directions.append('east')

                    if game_map[y_axis][x_axis - 1] != -1:    # check west
                        possible_directions.append('west')

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

            my_location = Location( position,       # create a location object with the following data
                                    element[1],
                                    element[2],
                                    element[3],
                                    available_directions,
                                    items)

            if position in locations_final:   # put that location into the dict under its position
                    locations_final[position] = my_location
            else:
                locations_final[position] = []
                locations_final[position] = my_location

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
location = my_world.get_location(1, 2)
print(location.available_actions())
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


