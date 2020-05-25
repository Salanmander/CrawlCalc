class Weapon:
    def __init__(self, dmg, acc, category,
                 name = 'weapon',
                 slay = 0,
                 st_bonus = 0,
                 brand = 'none'):
        self.name = name
        self.dmg = dmg
        self.acc = acc
        self.slay = slay
        self.st_bonus = st_bonus
        self.brand = brand
        self.category = category
        
