#!/bin/python

######################################################################################
#                           file piproximator.py                                     #
#                                                                                    #
#                                 MIT License                                        #
#                                                                                    #
#                        Copyright (c) 2026 PaperFox56                               #
#                                                                                    #
#   Permission is hereby granted, free of charge, to any person obtaining a copy     #
#   of this software and associated documentation files (the "Software"), to deal    #
#   in the Software without restriction, including without limitation the rights     #
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell        #
#   copies of the Software, and to permit persons to whom the Software is            #
#   furnished to do so, subject to the following conditions:                         #
#                                                                                    #
#   The above copyright notice and this permission notice shall be included in all   #
#   copies or substantial portions of the Software.                                  #
#                                                                                    #
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR       #
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,         #
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE      #
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER           #
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,    #
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE    #
#   SOFTWARE.                                                                        #
######################################################################################


from math import log10
import numpy as np

# Best meal known to mathkind
pie = 3.141592653589793 


def compute_pi(numerator: int, denominator: int, precision: int) -> tuple[int, int]:
    """
    Iteratively refines a rational approximation of π.

    At each iteration:
    - Exactly ONE new digit is committed to the numerator and/or denominator.
    - Several digits (default: 3) are temporarily explored as lookahead.
    - The lookahead allows choosing a digit that will still be good
      a few steps into the future (chess-style evaluation).
    - Extra digits are discarded after the choice is made.

    The process stops once the denominator reaches the requested precision.
    """

    # Number of digits explored ahead before committing a single digit.
    # This is NOT the number of digits added permanently.
    LOOKAHEAD_DIGITS = 3

    # Count how many base-10 digits the denominator currently has
    denom_digit_count = int(log10(denominator)) + 1

    # If the denominator already exceeds the allowed precision,
    # truncate it to fit the limit.
    diff = denom_digit_count - precision
    if denom_digit_count > precision:
        denominator //= 10 ** diff
        denom_digit_count = precision

    while True:
        # Logarithm of the current ratio gives us its order of magnitude.
        # This is used to decide whether the fraction is too small,
        # too large, or roughly in the right scale.
        ratio_log10 = log10(numerator / denominator)

        # a, c: how many digits we *temporarily append* to numerator / denominator
        # b, d: how many powers of 10 we apply as scaling compensation
        a = b = c = d = 0

        if ratio_log10 < 0:
            # Approximation is too small:
            # we want to grow the numerator faster than the denominator.
            a = LOOKAHEAD_DIGITS
            b = -min(0, int(ratio_log10) + LOOKAHEAD_DIGITS)

            c = max(0, int(ratio_log10) + LOOKAHEAD_DIGITS)
            d = 0

        elif ratio_log10 >= 1:
            # Approximation is too large:
            # we want to grow the denominator faster.
            denom_digit_count = int(log10(denominator)) + 1
            if denom_digit_count >= precision:
                break

            a = -min(0, int(ratio_log10) - LOOKAHEAD_DIGITS)
            b = 0

            c = LOOKAHEAD_DIGITS
            d = max(0, int(ratio_log10) - LOOKAHEAD_DIGITS)

        else:
            # Approximation is in the correct order of magnitude.
            # We refine both numerator and denominator symmetrically.
            denom_digit_count = int(log10(denominator)) + 1
            if denom_digit_count >= precision:
                break

            a = LOOKAHEAD_DIGITS
            c = LOOKAHEAD_DIGITS
            b = d = 0

        # Generate all digit combinations for the lookahead.
        # These represent future possibilities, not permanent changes.
        r1 = np.array([np.arange(10 ** a)])
        r2 = np.array([np.arange(10 ** c)])

        # Build candidate numerators and denominators by appending digits.
        num_candidates = numerator * 10 ** a + r1
        denom_candidates = denominator * 10 ** c + r2

        # Evaluate all candidate fractions against π.
        # The scaling by 10**b and 10**d compensates for magnitude mismatches.
        cost = (num_candidates * 10 ** b) * (
            1 / (denom_candidates * 10 ** d)
        ).transpose()

        # Absolute error from π for each candidate
        cost = abs(cost - pie)

        # Find the best candidate in the lookahead space
        m = cost.argmin()
        x = m % (10 ** a)
        y = m // (10 ** a)

        # Commit the BEST candidate found
        numerator = int(num_candidates[0, x])
        denominator = int(denom_candidates[0, y])

        # Debug output showing which digit pattern was explored
        print("n = " + "X" * a + "0" * b)
        print("d = " + "X" * c + "0" * d)
        print(numerator, denominator)

        # DISCARD lookahead digits:
        # only ONE digit effectively survives per iteration.
        numerator //= 10 ** min(a, LOOKAHEAD_DIGITS - 1)
        denominator //= 10 ** min(c, LOOKAHEAD_DIGITS - 1)

        print(numerator, denominator)

    return numerator, denominator


if __name__ == "__main__":
    def get_integer_input(prompts: list) -> list:
        """ Helper function to make sure the user understands you want positive integers as an input """
        result = []

        for prompt in prompts:
            i = input("Enter "+prompt+": ")
            while not i.isdigit():
                i = input("Please, "+prompt+" must be a positive integer, retry: ")

            result.append(int(i))

        return result

    num, denom, prec = 31, 1, 17

    num, denom, prec = get_integer_input([
        "the most significant digits of the numerator",
        "the most significant digits of the denominator",
        "the precision of the aproximation",
    ])
    # Compute a approximate version of the real pie
    num, denom = compute_pi(num, denom, prec)
    pi = num / denom

    print(f"PI = {num}/{denom} or {pi}")
    print(f"Error is {abs(pie-pi)}")
