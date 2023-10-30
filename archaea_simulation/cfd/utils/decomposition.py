def is_prime(num: int):
    if num > 1:
    # Iterate from 2 to n / 2
        for i in range(2, int(num/2)+1):
            # If num is divisible by any number between
            # 2 and n / 2, it is not prime
            if (num % i) == 0:
                return False
        else:
            return True
    else:
        return False
    
def distribute_cores(number_of_cores: int):
    x = 1
    y = 1
    z = 1
    noc = number_of_cores

    if is_prime(number_of_cores):
        return x, y, z * number_of_cores

    while not is_prime(noc):
        # Find the largest divisor of cores that is less than or equal to the square root of cores
        divisor = 1
        for i in range(2, int(noc**0.5) + 1):
            if noc % i == 0:
                divisor = i
        
        if x > y:
            y = y * divisor
        else:
            x = x * divisor

        z = noc / divisor
        noc = noc / divisor

    return int(x), int(y), int(z)

def hiearchical_coeffs(number_of_cores: int):
    x, y, z = distribute_cores(number_of_cores)
    return 'hierarchicalCoeffs\n' \
           '    {{\n' \
           '\tn ({0} {1} {2});\n' \
           '\torder xyz;\n' \
           '    }}\n'.format(x, y, z)  # noqa: UP030
    