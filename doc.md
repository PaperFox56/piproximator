# Rational pi Approximation - Algorithm Overview

## Goal

The goal of this algorithm is to build a rational approximation of pi of the form:

> π = N / D

where `N` and `D` are integers, and the approximation is refined one digit at a time.

This is not meant to be an optimal or formal numerical method, but a playful experimental algorithm, exploring how far a local, greedy digit-based search can go when approximating an irrational number.

---

## Core Idea

At each iteration, the algorithm:

- Commits to exactly one new decimal digit in the numerator and/or denominator.
- Before committing that digit, it looks ahead several digits (by default 3) to evaluate which choice will lead to the best approximation of π.
- Chooses the digit that minimizes the absolute error with respect to pi.
- Discards the extra lookahead digits, keeping only the single committed digit.

This is similar in spirit to chess engines: many candidate futures are evaluated, but only the first move is actually played.

---

## Lookahead Mechanism

Although only one digit is added per iteration, the algorithm temporarily explores a larger search space:

- It appends up to *k* digits (e.g. 3) to the numerator and/or denominator.
- It evaluates *all* combinations of those appended digits.
- It computes the resulting rational values and compares them to π.
- It selects the candidate with the smallest absolute error.

After this selection:

- Only the most significant of the newly added digits is kept.
- The remaining lookahead digits are discarded.

This allows the algorithm to avoid locally good but globally bad digit choices.

---

## Scaling Logic

The algorithm monitors the order of magnitude of the current approximation:

- If `N / D` is too small, it prioritizes growing the numerator.
- If `N / D` is too large, it prioritizes growing the denominator.
- If the ratio is close to the correct magnitude, it refines both sides symmetrically.

This decision is driven by the base-10 logarithm of the ratio.

---

## Precision Control

To prevent uncontrolled growth:

- The denominator is limited to a maximum number of digits (`precision`).
- If this limit is reached, the algorithm stops.
- Intermediate candidates may temporarily exceed the limit during lookahead, but the committed state always respects it.

---

## What this is not

This algorithm is best understood as a numerical toy or a thought experiment, not as a replacement for established approximation techniques.

---

## Code-Level Commentary

Although the algorithm description above is intentionally code-agnostic, a few implementation details are worth documenting because they shape how the algorithm behaves in practice.

### Lookahead vs Commitment

In the code, this distinction appears through two phases:

1. **Expansion phase**
   - Multiple digits (e.g. 3) are appended to the numerator and/or denominator.
   - All possible combinations of those digits are generated using vectorized NumPy arrays.
   - This phase explores *possible futures*.

2. **Truncation phase**
   - After the best candidate is selected, most of the newly added digits are removed.
   - Only the most significant digit of the lookahead survives.
   - This ensures that exactly **one digit per iteration** is truly committed.

This mirrors a depth-limited search where only the first move is applied.

---

### Role of the Logarithm

The use of `log10(numerator / denominator)` is not about precision, but scale detection:

- A negative value means the ratio is too small (N < D).
- A value greater than or equal to 1 means the ratio is too large (N >= 10\*D).
- Values in between indicate the ratio is in the correct order of magnitude.

This allows the algorithm to decide where digits should be added before refinement.

---

### Digit Parameters (`a`, `b`, `c`, `d`)

Note: If someone has better names for these ones I'm all ears.

In the implementation, four integer parameters control digit manipulation:

- `a`: number of digits temporarily appended to the numerator
- `c`: number of digits temporarily appended to the denominator
- `b`: power-of-10 scaling applied to the numerator
- `d`: power-of-10 scaling applied to the denominator

Together, they allow the algorithm to explore candidates that differ both in value and scale, without permanently committing to those changes.

---

### Why NumPy Is Used

NumPy is not required conceptually, but it enables:

- Exhaustive evaluation of all digit combinations in the lookahead window
- Simple expression of a 2D cost surface
- Efficient minimum selection across all candidates

This keeps the implementation compact and readable.

---

### Debug Output

The printed patterns such as:

```
n = XXX0
d = XX
```

are meant to visualize:

- How many digits are being explored (`X`)
- How scaling is applied (`0`)

They are diagnostic tools and not part of the algorithm’s logic.

---

## Non-Goals

- Guaranteed optimal convergence
- Performance efficiency
- Mathematical optimality or proofs

The fun lies in watching the approximation evolve, not in beating existing methods.


## Improvement goals

The current implementation suffers from several limitations. The most significant one is precision. Python uses 64-bit floating-point numbers, which limits not only the accuracy of intermediate calculations, but also the precision of the reference value of pi stored in the code.

Additionally, NumPy relies on 64-bit integers for array computations, which caused integer overflows during testing. For this reason, it is recommended not to use values larger than 17 for the precision parameter.