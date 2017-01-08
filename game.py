"""
Classes for the set game itself.
A card on the game board.
The game board.
  - can run solve() to return valid sets
"""

from itertools import combinations

shapes = ["diamond", "oval", "wiggle"]
numbers = [1, 2, 3]
fillings = ["empty", "lines", "full"]
colors = ["red", "green", "purple"]


class Card(object):

    def __init__(self, shape, number, filling, color):
        if shape not in shapes:
            raise Exception("invalid shape")
        if number not in numbers:
            raise Exception("invalid number")
        if filling not in fillings:
            raise Exception("invalid filling")
        if color not in colors:
            raise Exception("invalid color")

        self.fields = {}
        self.fields['shape'] = shape
        self.fields['number'] = number
        self.fields['filling'] = filling
        self.fields['color'] = color

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "{number} {color} {filling} {shape}".format(**self.fields)


class Game(object):

    def __init__(self):
        self.cards = set()

    def addCard(self, new_card):
        self.cards.add(new_card)

    # solves a given set game
    def solve(self):
        for c in self.cards:
            print(c.__dict__)

        sets = findSets(self.cards)

        print "Sets found = {}".format(len(sets))
        for s in sets:
            print "Set!"
            for c in s:
                print(c)
            print ""

        return sets


def isValidSet(cards):
    # all same?
    for f in ['shape', 'color', 'filling', 'number']:

        pair1 = cards[0].fields[f] == cards[1].fields[f]
        pair2 = cards[1].fields[f] == cards[2].fields[f]
        pair3 = cards[2].fields[f] == cards[0].fields[f]

        # check if all same OR all different
        if (pair1 and pair2 and pair3) or not (pair1 or pair2 or pair3):
            continue
        return False

    return True


def findSets(cards):
    # make all combinations of 3
    combs = combinations(cards, 3)

    # check if they're sets
    validSets = []
    for c in combs:
        if isValidSet(c):
            validSets.append(c)

    # return sets
    return validSets

# -------
# Example
# -------


def ExampleGame():
    g = Game()

    # TODO: Get these cards via image detection :P
    # e.g. this is from here:
    # https://www.dropbox.com/s/77ut9dkv9hq4pki/Screenshot%202016-03-05%2018.48.31.png?dl=0

    # more options
    # https://www.dropbox.com/s/k6o7snm1jl7jg5e/Screenshot%202016-03-05%2018.56.06.png?dl=0
    # http://i.stack.imgur.com/ykW6n.png
    # https://whieldon.files.wordpress.com/2013/08/set_solid.png

    # maybe
    # http://www.pyimagesearch.com/2014/10/20/finding-shapes-images-using-python-opencv/
    g.addCard(Card("oval", 2, "empty", "green"))
    g.addCard(Card("wiggle", 1, "empty", "green"))
    g.addCard(Card("diamond", 3, "lines", "green"))
    g.addCard(Card("diamond", 3, "empty", "purple"))

    g.addCard(Card("wiggle", 2, "empty", "red"))
    g.addCard(Card("wiggle", 1, "full", "purple"))
    g.addCard(Card("oval", 1, "lines", "red"))
    g.addCard(Card("diamond", 3, "empty", "red"))

    g.addCard(Card("diamond", 2, "full", "purple"))
    g.addCard(Card("diamond", 3, "full", "red"))
    g.addCard(Card("oval", 2, "lines", "green"))
    g.addCard(Card("diamond", 3, "empty", "green"))

    return g
