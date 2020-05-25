import random
from crawl_random import *

class Monster:
    def __init__(self, ac = 0,
                 ev = 0):
        self.ac = ac
        self.ev = ev

    def ac_roll(self):
        return roll(1 + self.ac)

    def get_hit(self, to_hit):
        # 2.5% chance each of auto hit or miss
        this_roll = random.random()
        if(this_roll < 0.025):
            return True
        elif(this_roll < 0.05):
            return False
        
        
        this_ev = (roll(2 * self.ev) + roll(2 * self.ev))//2

        margin = to_hit - this_ev
        return margin >= 0

    
        
