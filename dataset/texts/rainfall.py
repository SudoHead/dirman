# Design a program called rainfall that consumes a list of numbers
# representing daily rainfall amounts as entered by a user. The list may
# contain the number -999 indicating the end of the data of interest.
# Produce the average of the non-negative values in the list up to the
# first -999 (if it shows up). There may be negative numbers other than
# -999 in the list.

from functools import reduce

def average_rainfall(input_list):
    # Here is where your code should go
    s=e=0
    for x in input_list :
        if x == -999:
            break
        elif x > 0:
            s += x
            e += 1
    return s/e

# Don't touch anything below this line.
if __name__ == "__main__":
    import sys

    # We get the arguments assuming that they are a list of *integers*
    rainfall_measurements = list(map(int, sys.argv[1:]))

    # We print the average.
    print(average_rainfall(rainfall_measurements))
