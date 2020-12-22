import string, random


def rand_PINCode(size):
    # Takes random choices from
    generate_pass = ''.join([random.choice(string.digits)
                             for n in range(size)])

    return generate_pass
