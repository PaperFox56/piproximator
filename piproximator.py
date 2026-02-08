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

# Best meal known to mathkind
pie = 3.141592653589793 


def compute_pi(numerator: int, denominator: int, precision:int) -> int:
    """
The algorithm works as follows.

First, we troncate the denominator to fit in the given precision, the alogoritm stops once no better aproximation can be found without adding a digit to the denominator.

Next we need to detect if the numerator is smaller than the denominator, in which case we need to increase it to the next level of magnitude. This is done by adding a digit at the end while staying as close to pi as posible.

The same is done if the denominator is 10 times (or more) smaller than the numerator.

Finally, when the two numbers have in same relative size, we just add one digit to each number.
"""
    denom_digit_count = int(log10(denominator)) + 1

    if denom_digit_count > precision:
        diff = denom_digit_count - precision
        denominator = denominator // 10**diff

    while True:
        denom_digit_count = int(log10(denominator)) + 1
        ratio = numerator / denominator
        

        if ratio < 1:  # We need to buff the numerator
            best = -1
            cost = ratio * 100  # magic

            for i in range(10):
                n = numerator * 10 + i
                n_cost = abs(n / denominator - pie)
                
                if n_cost < cost:
                    best = n
                    cost = n_cost

            numerator = best

        elif ratio >= 10: # We need to buff the denominator
            if denom_digit_count >= precision:
                break

            best = -1
            cost = ratio * 100  # magic

            for i in range(10):
                d = denominator * 10 + i
                n_cost = abs(numerator / d - pie)
                
                if n_cost < cost:
                    best = d
                    cost = n_cost

            denominator = best

        else:
            # find the best way to a one digit to each number while keeping the ratio close to pi
            if denom_digit_count >= precision:
                break

            best = (-1, -1)
            cost = 100  # any number above 10 is honestly fine here

            for i in range(10):
                d = denominator * 10 + i
                for j in range(10):
                    n = numerator * 10 + j
                    n_cost = abs(n / d - pie)
                
                    if n_cost < cost:
                        best = n, d
                        cost = n_cost

            numerator = best[0]
            denominator = best[1]

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

    #num, denom, prec = 3, 1, 10

    num, denom, prec = get_integer_input([
        "the most significant digits of the numerator",
        "the most significant digits of the denominator",
        "the precision of the aproximation",
    ])
    # Compute a approximate version of the real pie
    num, denom = compute_pi(num, denom, prec)

    print(f"PI = {num}/{denom} or {num/denom}")
