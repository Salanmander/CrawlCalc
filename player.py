from crawl_random import *

class Player:
    def __init__(self, strength = 10,
                 dex = 10,
                 skills = {},
                 size = 'medium',
                 extra_slay = 0,
                 encumberance_rating = 0,
                 base_shield_penalty = 0):
        self.strength = strength
        self.dex = dex


        if('armor' in skills):
            skills['armour'] = skills['armor']
        self.skills = skills
        
        self.extra_slay = extra_slay
        self.size = size
        self.encumber = encumberance_rating
        self.sh_penalty = base_shield_penalty


    def set_skill(self, skill_name, value):
        if skill_name == 'armor':
            skill_name = 'armour'
        self.skills[skill_name] = value
        

    def get_skill(self, skill_name):
        # Return skill, defaults to 0 if has not been added
        return self.skills.get(skill_name, 0)


    def get_weapon_skill(self, weapon):
        skill_name = weapon.category
        return self.get_skill(skill_name)


    def get_to_hit(self, weapon):

        # Base
        to_hit = 15 + self.dex//2

        # Skills multiply by 100 before roll, then divide by 100, so that
        # non-integer skill increases the probability of the highest number
        
        # Fighting skill
        to_hit += roll(self.get_skill('fighting') * 100) // 100

        # Weapon skill
        to_hit += roll(self.get_weapon_skill(weapon) * 100) // 100

        # Weapon bonus and slaying
        to_hit += weapon.acc + weapon.slay + self.extra_slay

        # armour and shield use a scale factor to make die rolls more granular
        # can't this game just learn about floats!?!??
        armour_die = self.get_armour_penalty() * 20
        armour_roll = div_rand_round(roll_die(armour_die), 20)
        
        to_hit -= armour_roll

        shield_die = self.get_shield_penalty() * 20
        shield_roll = div_rand_round(roll_die(shield_die), 20)

        to_hit -= shield_roll

        return roll(to_hit)


    def get_shield_penalty(self):
        skill = self.get_skill('shields')
            
        penalty = self.sh_penalty - skill/(5 + self.get_size_factor())
        return max(0, penalty)

    def get_armour_penalty(self):
        armr = self.encumber * self.encumber
        sk_effect = (450 - self.get_skill('armour')*10) / 450
        st_effect = 1/(self.strength + 3)
        return (2/5) * armr * sk_effect * st_effect


    def get_size_factor(self):
        if self.size == 'little':
            return 4
        elif self.size == 'small':
            return 2
        elif self.size == 'medium' or self.size == 'normal':
            return 0
        elif self.size == 'large':
            return -2
        else:
            return None
