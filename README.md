## Pi-proximator

This program compute the best fractional aproximation of pi (the mathematical constant) using two numbers given as prompt.

The usage is simple. When you launch the program, you will be promted to give two integers as well as the precision you want for the approximation (the precision is the lenght in digits of the denominator of the fraction).


The first number given is used as most significative part of the numerator while the second digit is used for the denominator. The program then computes the best approximation of pi by adding digits to each part of the fraction.


### Limits

The current version uses a naive algorithm where the digits are chosen one after another. This cause really poor precision in the approximation.

In the the next iteration, I will implement a more advanced algorithm allowing to choose a digit based while predicting the following ones in advance, thus increasing precision.


# Usage

Clone this git repo:

```bash
git clone https://github.com/PaperFox56/piproximator
cd piproximator
```

or simply download the python script.

You can start it with a python interpreter

```
<your_python_interpreter> piproximator.py  
```

or make it executable and start it as any program:

```
chmod +x piproximator.py
./piproximator.py
```
