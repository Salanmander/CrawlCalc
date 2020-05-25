import random

# Equivalent to the random2() method in Crawl source random.cc
# Returns uniformly distributed int in range [0, floor(top)-1]
def roll(top):
    if top <= 1:
        return 0
    
    return random.randrange(int(top))
    

# Returns int in range [1, size]
# if 0 < size < 2, returns 1
# if size <= 0 returns 0
def roll_die(size):
    if size <= 0:
        return 0
    else:
        return 1 + roll(size)


# Returns int, with probability of rounding up or down based on
# fraction of the way in between.
def div_rand_round(num, denom):
    whole = num // denom
    rem = num % denom

    if rem == 0:
        return whole
    else:
        if roll(denom) < rem:
            return whole + 1
        else:
            return whole
        
    
