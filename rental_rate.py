import math
import sys

def rate(interests, rent, fee, tax, invest):
    income = rent * 10
    out = interests * 12 + fee * 12 + tax * 4
    return (income - out) / invest * 100


if __name__ == "__main__":
    rent = int(sys.argv[1])
    
    interests = 366.74
    fee = 435.
    tax = 1192.75
    invest = 250000. - 145889.19

    print(rate(interests, rent, fee, tax, invest))
    
