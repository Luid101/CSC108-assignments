class Player:

    def __init__(self, x, y):
        '''
        Creates a new Player.
        :param x: x-coordinate of position on map
        :param y: y-coordinate of position on map
        :return:none

        This is a suggested starter class for Player.
        You may add new parameters / attributes / methods to this class as you see fit.
        Consider every method in this Player class as a "suggested method":
                -- Suggested Method (You may remove/modify/rename these as you like) --
        '''

        self.x = x
        self.y = y
        self.inventory = []
        self.victory = False
        self.defeat = False
        self.score = 0
        self.total_moves = 0

    def move(self, dx, dy):
        '''
        Given integers dx and dy, move player to new location (self.x + dx, self.y + dy)
        :param dx: change in x
        :param dy: change in y
        :return:none
        '''

        self.x += dx
        self.y += dy

    def move_north(self):
        '''These integer directions are based on how the map must be stored
        in our nested list World.map'''
        self.move(0,-1)

    def move_south(self):
        self.move(0,1)

    def move_east(self):
        self.move(1,0)

    def move_west(self):
        self.move(-1,0)

    def add_item(self, item):
        '''
        Add item to inventory.
        :param item:
        :return:
        '''

        self.inventory.append(item)

    def remove_item(self, item):
        '''
        Remove item from inventory.
        :param item:
        :return:
        '''

        self.inventory.remove(item)

    def get_inventory(self):
        '''
        Return inventory.
        :return:
        '''

        inventory = []

        for item in self.inventory:
            inventory.append(item.get_name())

        return inventory

    def get_item(self, item_name):
        """
        takes an item name and gets back the item if it exists else return false
        :param item_name: the name of an item
        :return: return the item if it is present and False if not
        """
        if len(self.inventory) > 0:                         # if there is at least one item in that location
            for element in self.inventory:
                if element.get_name() == item_name:
                    return element
            return False
        else:
            return False

    def add_move(self):
        """
        add one to the total number of moves made
        :return:
        """

        self.total_moves += 1

    def get_position(self):
        """
        return the position that the player is in, in the map
        :return:
        """
        return [self.x, self.y]

