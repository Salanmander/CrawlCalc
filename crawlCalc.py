import random
import statistics

def main():
    num_trials = 10000
    
    weap1_base = 12
    weap1_slay = 7
    weap1_st_bonus = 0
    weap1_brand = "electrocution"

    weap2_base = 13
    weap2_slay = 3
    weap2_st_bonus = 0
    weap2_brand = "holy wrath"

    st = 27
    wp_skill = 14
    ft_skill = 11.9
    extra_slay = 3

    enemy_ac = 0
    
    dmg_list = []
    for _ in range(num_trials):
        dmg =  final_damage(weap1_base, st + weap1_st_bonus,
                            wp_skill, ft_skill,
                            weap1_slay, enemy_ac,
                            weap1_brand)
        dmg_list.append(dmg)
        

    dmg1 = statistics.mean(dmg_list)

    
    dmg_list = []
    for _ in range(num_trials):
        dmg =  final_damage(weap2_base, st + weap2_st_bonus,
                            wp_skill, ft_skill,
                            weap2_slay, enemy_ac,
                            weap2_brand)
        dmg_list.append(dmg)
        

    dmg2 = statistics.mean(dmg_list)

    print("Weap 1: " + str(dmg1))
    print("Weap 2: " + str(dmg2))

 
# Weapon damage after accounting for AC and brands
def final_damage(base, st, wp_skill, ft_skill, slay, ac, brand = "none"):
    damage = damage_roll(base, st, wp_skill, ft_skill, slay)
    reduce = ac_roll(ac)

    damage_done = max(0, damage-reduce)

    brand_damage = calc_brand_damage(damage_done, brand)

    return damage_done + brand_damage


# Weapon damage before AC
def damage_roll(base, st, wp_skill, ft_skill, slay):

    # Calculate strength modifier
    str_mod = 39
    if st > 10:
        str_mod += 2*(roll(st-9))
    elif st < 10:
        str_mod -= 3*(roll(11-st))
    str_mod /= 39

    # Calculate skill modifiers
    wp_mod = (2500 + roll(100*wp_skill + 1))/2500
    ft_mod = (3000 + roll(100*ft_skill + 1))/3000


    # Roll damage
    dmg = roll(base * str_mod + 1) -1

    # Roll slaying
    slay_bonus = roll(1+slay)

    # Apply modifiers
    dmg = dmg * wp_mod * ft_mod + slay_bonus

    
    return dmg


# Damage from just the brand
def calc_brand_damage(damage_done, brand):
    if brand == "electrocution":
        # 1 in 3 chance
        if(random.random() * 3 < 1):
            return 8 + roll(13)
        else:
            return 0

    if damage_done <= 0:
        return 0

    # Brands after this require some normal damage to do anything
    if brand == "flaming" or brand == "freezing":
        return 1 + roll(damage_done)//2

    elif brand == "holy wrath":
        return 1 + roll(damage_done * 15)//10

    elif brand == "antimagic":
        return 0

    elif brand == "vorpal":
        return 1 + roll(damage_done)//3

    elif brand == "vampirism":
        return 0
        
    else:
        return 0


def ac_roll(ac):
    return roll(1+ac)


# Equivalent to the random2() method in Crawl source random.cc
# Returns uniformly distributed int in range [0, floor(top)-1]
def roll(top):
    if top <= 1:
        return 0
    
    return random.randrange(int(top))
    


if __name__ == "__main__":
    main()
