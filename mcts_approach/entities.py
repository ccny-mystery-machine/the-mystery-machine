class Actor:
    """The main characters of the story"""

    def __init__(self, name, occupation="citizen", place="outside"):
        self.name = name
        self.occupation = occupation
        self.place = place
        self.items = []

    def __str__(self):
        return self.name

class Item:
    """Available items in the story"""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Place:
    """Available places in the story"""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

actors = {}
items = {}
places = {}

# 5 actors
actors["Alice"] = Actor("Alice")
actors["Bob"] = Actor("Bob")
actors["Charlie"] = Actor("Charlie")
actors["Sherlock"] = Actor("Sherlock", "detective")
actors["Lestrade"] = Actor("Lestrade", "inspector")

# 3 items
items["gun"] = Item("gun")
items["vase"] = Item("vase")
items["baseball_bat"] = Item("baseball bat")

# 2 places
places["outside"] = Place("outside")
places["house"] = Place("house")
places["jail"] = Place("jail")
