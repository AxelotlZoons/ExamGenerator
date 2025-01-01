""" Some generic functions useful to make the tutorials, the exam and the resit."""
import numpy as np

private_seed = "my_private_seed.txt"

def weighted_choice(weights, gen):
    """Select the index of an array of weights, proportional to
    the weights in the array weights."""
    rnd = gen.uniform() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i

def weighted_sample(a, w, k, gen):
    """Get k samples without replacement from a in which each element is selected
    according to the weights in w."""
    if len(a) != len(w):
        raise ValueError("The Lengths of lists don't match.")

    w = list(w)  # make a copy of w
    r = []  # contains the random shuffle
    for i in range(k):
        j = weighted_choice(w, gen)
        r.append(a[j])
        w[j] = 0
    return r

def get_random_generator(number):
    """I want to set the seed of a np.random.default_gen in a deterministic
    way, but without disclosing it to others."""
    with open(private_seed, "r") as fp:
        seed = int(fp.readline())
    return np.random.default_rng(seed + number)
