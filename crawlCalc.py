import random
import statistics

def main():
    num_trials = 10000
    print_histograms = True
    histogram_bins = 10

    weapons = []
    
    weapons.append({'name': 'trishula',
                    'base': 13,
                    'slay': 9,
                    'st_bonus': 0,
                    'brand': 'none',
                    'skill': 17.9})

    
    weapons.append({'name': 'demon trident',
                    'base': 12,
                    'slay': 9,
                    'st_bonus': 0,
                    'brand': 'electrocution',
                    'skill': 17.9})
    """

    weapons.append({'name': 'antimagic spear',
                    'base': 6,
                    'slay': 5,
                    'st_bonus': 4,
                    'brand': 'none',
                    'skill': 27})
    
    weapons.append({'name': 'antimagic trident',
                    'base': 9,
                    'slay': 0,
                    'st_bonus': 0,
                    'brand': 'none',
                    'skill': 27})
    """

    st = 31
    dex = 10
    ft_skill = 23.5
    extra_slay = 3

    enemy_ac = 0

    for weap in weapons:
        dmg_list = []
        for _ in range(num_trials):
            dmg =  final_damage(weap['base'], st + weap['st_bonus'],
                                weap['skill'], ft_skill,
                                weap['slay'] + extra_slay, enemy_ac,
                                weap['brand'])
            dmg_list.append(dmg)
            
        dmg1 = statistics.mean(dmg_list)

        print("\n\n" + weap['name'] + ": " + str(dmg1) + "\n")
        
        if print_histograms:
            print_histogram(dmg_list, histogram_bins)


# Prints the percentage of elements in the list that fall into each bin.
# Bin sizes are uniform, except for the bin of exactly-zero.
# Total number of bins is given by num_bins, so size of non-zero bins is
# max_val/(num_bins - 1)
def print_histogram(values, num_bins):
    values.sort()
    num_vals = len(values)

    max_val = values[-1]

    bin_tops = get_integer_histogram_bins(max_val, num_bins)


    curr_index = 0
    
    for i in range(num_bins):
        if i == 0:
            bin_min = 0
        else:
            bin_min = bin_tops[i-1] + 1

        bin_max = bin_tops[i]

        num_in_bin = 0
        
        if i == num_bins-1:
            num_in_bin = (num_vals) - curr_index
        else:
            # Find the beginning and end of the range
            bin_start_index = curr_index
            while(values[curr_index] <= bin_max):
                curr_index += 1

            num_in_bin = curr_index - bin_start_index

        percent_str = str(round(100*num_in_bin/num_vals, 2)) + "%"
        print("{:2d} - {:2d}: ".format(bin_min, bin_max) + percent_str)


# Returns a list with num_bins values, representing the high end of bins for
# a histogram. The first value is always 0, and the last value is always
# max_val. num_bins must be at least 2.
#
# When max_val doesn't divide evenly, the remainder increases the size of
# the appropriate number of bins at the top end of the range by 1
def get_integer_histogram_bins(max_val, num_bins):

    # The even spacing gets split across (num_bins - 1) bins
    spaced_bins = num_bins - 1
    small_bin_size = max_val // spaced_bins

    # The remainder is the number of bins that need to be large
    # So the number of bins that need to be small is the number
    # of bins with even spacing minus that
    small_bins = spaced_bins - max_val % (num_bins - 1)
    
    bin_tops = [0]

    for i in range(num_bins - 1):
        size = small_bin_size

        # if we need 3 small bins, then those are i = 0, 1, 2
        # Anything larger is a big bin
        if i >= small_bins:
            size += 1

        bin_tops.append(bin_tops[-1] + size)

    return bin_tops
        
    
    

 
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
    dmg = int(dmg * wp_mod)
    dmg = int(dmg * ft_mod)
    dmg = dmg + slay_bonus

    
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
        # (8 * dam) / (hitdice + 1) = duration increase
        # spell success chance of enemy is 4/(4 + duration)
        # Duration appears to be in turns
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
